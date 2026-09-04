"""
Feedback routes — anyone (logged in or anonymous) can submit feedback.
Admin can view submissions and mark them reviewed.

Includes a simple in-memory rate limit to prevent spam:
    - 1 submission per IP every COOLDOWN_SECONDS
    - max MAX_PER_DAY submissions per IP per rolling 24h

Note: this is in-memory, so it resets on every deploy/restart and does NOT
work correctly if you ever run multiple server instances/workers (each
instance would have its own counter). Fine for a single-instance Render
free/starter deployment; swap for a Redis- or DB-backed limiter if you scale
horizontally.
"""
import os
import time
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Header, Request, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Feedback, User
from app.schemas import FeedbackCreate, FeedbackOut, FeedbackResponse
from app.auth import get_optional_user, get_current_user
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter(prefix="/feedback", tags=["Feedback"])

ADMIN_SECRET = os.getenv("ADMIN_SECRET")

# ── Rate limit config ──
COOLDOWN_SECONDS = 60        # min gap between two submissions from the same IP
MAX_PER_DAY = 5              # max submissions per IP per rolling 24h
DAY_SECONDS = 24 * 60 * 60

# ip -> list of timestamps (epoch seconds) of recent submissions
_submission_log: dict[str, list[float]] = defaultdict(list)


def _client_ip(request: Request) -> str:
    """
    Best-effort client IP. Render sits behind a proxy, so prefer
    X-Forwarded-For (first hop) if present, else fall back to request.client.
    """
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _check_rate_limit(ip: str):
    now = time.time()
    timestamps = _submission_log[ip]

    # Drop anything older than 24h
    timestamps[:] = [t for t in timestamps if now - t < DAY_SECONDS]

    if timestamps and (now - timestamps[-1]) < COOLDOWN_SECONDS:
        wait = int(COOLDOWN_SECONDS - (now - timestamps[-1]))
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            f"Please wait {wait}s before submitting more feedback.",
        )

    if len(timestamps) >= MAX_PER_DAY:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "You've reached the daily feedback limit. Please try again tomorrow.",
        )

    timestamps.append(now)


def verify_admin(x_admin_secret: str = Header(...)):
    if not ADMIN_SECRET:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Admin access not configured.")
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid admin credentials.")
    return True


@router.post("/", response_model=FeedbackResponse)
def submit_feedback(
    payload: FeedbackCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """Submit feedback. Works whether or not the user is logged in. Rate-limited per IP."""
    ip = _client_ip(request)
    _check_rate_limit(ip)
    
    BANNED_WORDS = {
        "fuck", "shit", "bitch", "asshole", "porn", "sex", "cunt", 
        "dick", "cock", "pussy", "nigger", "faggot", "slut", "whore", 
        "bastard", "nude", "naked", "abuse"
    }
    
    text_to_check = ((payload.message or "") + " " + (payload.name or "")).lower()
    if any(word in text_to_check for word in BANNED_WORDS):
        raise HTTPException(status_code=400, detail="Feedback contains inappropriate language and violates our Terms & Conditions.")


    fb = Feedback(
        user_id=current_user.id if current_user else None,
        name=payload.name or (current_user.name if current_user else None),
        email=payload.email or (current_user.email if current_user else None),
        category=payload.category,
        message=payload.message,
        rating=payload.rating,
        page_context=payload.page_context,
        parent_id=getattr(payload, 'parent_id', None),
        image_data=getattr(payload, 'image_data', None),
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return FeedbackResponse(message="Thanks for the feedback! 🙌", id=fb.id)


@router.get("/", response_model=list[FeedbackOut])
def list_feedback(_: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: list all feedback, newest first."""
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()


@router.post("/{feedback_id}/resolve", response_model=FeedbackResponse)
def mark_resolved(feedback_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: mark a feedback item as reviewed."""
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(404, "Feedback not found.")
    fb.status = "reviewed"
    db.commit()
    return FeedbackResponse(message="Marked as reviewed.", id=fb.id)


@router.get("/public", response_model=list[FeedbackOut])
def list_public_feedback(db: Session = Depends(get_db)):
    """Public: list all feedback to display as reviews."""
    # Fetch all visible feedback/replies
    fb = db.query(Feedback).filter(Feedback.status != "hidden").order_by(Feedback.helpful_votes.desc(), Feedback.created_at.desc()).all()
    # Mask emails for privacy
    for f in fb:
        f.email = None
    return fb

@router.delete("/{feedback_id}", response_model=FeedbackResponse)
def delete_feedback(feedback_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: delete a feedback item."""
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(404, "Feedback not found.")
    db.delete(fb)
    db.commit()
    return FeedbackResponse(message="Feedback deleted.", id=feedback_id)

@router.post("/{feedback_id}/helpful", response_model=FeedbackResponse)
def mark_helpful(feedback_id: int, db: Session = Depends(get_db)):
    """Public: mark a feedback item as helpful."""
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(404, "Feedback not found.")
    fb.helpful_votes = (fb.helpful_votes or 0) + 1
    db.commit()
    return FeedbackResponse(message="Marked as helpful.", id=fb.id)

@router.patch("/{feedback_id}/visibility", response_model=FeedbackResponse)
def toggle_visibility(feedback_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(404, "Not found")
    fb.status = "hidden" if fb.status != "hidden" else "new"
    db.commit()
    return FeedbackResponse(message=f"Visibility toggled", id=fb.id)


from pydantic import BaseModel
class AdminReplyPayload(BaseModel):
    reply_text: str

def send_email_async(user_email: str, reply_text: str, feedback_message: str):
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    sender_email = os.getenv("SMTP_EMAIL", "no-reply@matdatahub.com")
    sender_password = os.getenv("SMTP_PASSWORD", "")
    
    if not sender_password:
        return
        
    try:
        msg = MIMEMultipart()
        msg['From'] = f"MatDataHub Support <{sender_email}>"
        msg['To'] = user_email
        msg['Subject'] = "Admin Response to your Feedback on MatDataHub"
        
        body = f"Hi there!\n\nAn admin has reviewed and replied to your recent feedback/report:\n\nYour Feedback: \"{feedback_message}\"\n\nAdmin Reply:\n{reply_text}\n\nThanks for helping us improve MatDataHub!\n\nBest,\nThe MatDataHub Engineering Team"
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Strip spaces from App Password (users often copy it with spaces)
        sender_password = sender_password.replace(" ", "")
        
        import socket
        orig_getaddrinfo = socket.getaddrinfo
        def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
            return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
        socket.getaddrinfo = getaddrinfo_ipv4
        
        try:
            # Use SMTP_SSL on port 465 to bypass firewall/port blocks
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
        finally:
            socket.getaddrinfo = orig_getaddrinfo
        print(f"Successfully sent reply email to {user_email}")
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")

@router.post("/{feedback_id}/reply")
def reply_to_feedback(
    feedback_id: int,
    payload: AdminReplyPayload,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    reply_text = payload.reply_text
    
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
        
    # Overwrite the admin_reply field with the newest reply
    feedback.admin_reply = reply_text
    feedback.status = "reviewed"
    db.commit()
    db.refresh(feedback)
    
    # Resolve user email
    user_email = feedback.email
    if not user_email and feedback.user_id:
        user_record = db.query(User).filter(User.id == feedback.user_id).first()
        if user_record:
            user_email = user_record.email
            
    if user_email:
        sender_password = os.getenv("SMTP_PASSWORD", "")
        if sender_password:
            background_tasks.add_task(send_email_async, user_email, reply_text, feedback.message)
            return {"ok": True, "message": "Reply saved & Email dispatched in background!"}
        else:
            return {"ok": True, "message": "Reply saved! (Email skipped: missing SMTP_PASSWORD on server)"}
            
    return {"ok": True, "message": "Reply saved! (No user email found to notify)"}
