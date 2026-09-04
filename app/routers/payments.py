import os
import hmac
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import razorpay

from app.database import get_db
from app.models import User
from app.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/payments", tags=["Payments"])

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")

# Initialize razorpay client only if keys are present
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)) if RAZORPAY_KEY_ID else None

class CreateLinkRequest(BaseModel):
    tier: str

@router.post("/create-link")
def create_payment_link(req: CreateLinkRequest, current_user: User = Depends(get_current_user)):
    if not client:
        raise HTTPException(status_code=500, detail="Razorpay is not configured on the server.")
        
    tier = req.tier.lower()
    if tier not in ["pro", "advanced"]:
        raise HTTPException(status_code=400, detail="Invalid tier.")
        
    amount = 49900 if tier == "pro" else 9999900  # Amount in paise (multiply INR by 100)
    
    # Generate payment link
    try:
        payment_link_data = {
            "amount": amount,
            "currency": "INR",
            "accept_partial": False,
            "description": f"Upgrade to {tier.capitalize()} Tier",
            "customer": {
                "name": current_user.name or "MatDataHub User",
                "email": current_user.email
            },
            "notify": {
                "sms": False,
                "email": True
            },
            "reminder_enable": False,
            "notes": {
                "user_id": str(current_user.id),
                "tier": tier
            },
            # "callback_url": "https://matdataapp-x5gof2igdr7cmiwucho22n.streamlit.app/", # Optional redirect
            # "callback_method": "get"
        }
        
        response = client.payment_link.create(payment_link_data)
        return {"payment_url": response.get("short_url")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create payment link: {str(e)}")

@router.post("/webhook")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Razorpay sends a webhook when payment succeeds.
    """
    webhook_signature = request.headers.get("X-Razorpay-Signature")
    if not webhook_signature:
        raise HTTPException(status_code=400, detail="Missing signature")
        
    body = await request.body()
    
    # Verify signature
    try:
        expected_sig = hmac.new(
            bytes(RAZORPAY_WEBHOOK_SECRET, 'utf-8'),
            msg=body,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_sig, webhook_signature):
            raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Signature verification failed")
        
    try:
        data = await request.json()
        event = data.get("event")
        
        if event == "payment_link.paid" or event == "payment.captured":
            # Payment link payloads store notes in data.payload.payment_link.entity.notes
            # or data.payload.payment.entity.notes depending on the event
            entity = data["payload"].get("payment_link", data["payload"].get("payment"))["entity"]
            notes = entity.get("notes", {})
            
            user_id_str = notes.get("user_id")
            tier = notes.get("tier")
            
            if user_id_str and tier:
                user_id = int(user_id_str)
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.tier = tier
                    user.upgrade_status = None
                    user.requested_tier = None
                    db.commit()
                    
        return {"status": "ok"}
    except Exception as e:
        # We return 200 even on processing errors so Razorpay doesn't endlessly retry if our logic fails,
        # but in production we'd want to log this securely.
        return {"status": "error", "detail": str(e)}
