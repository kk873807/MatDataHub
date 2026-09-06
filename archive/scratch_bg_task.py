import sys
import re

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to add BackgroundTasks import
if "from fastapi import BackgroundTasks" not in content:
    content = content.replace("from fastapi import APIRouter, HTTPException, Depends, Request, Header, status", 
                              "from fastapi import APIRouter, HTTPException, Depends, Request, Header, status, BackgroundTasks")

# Now rewrite the reply_to_feedback endpoint
old_route_start = "class AdminReplyPayload(BaseModel):"
# Find where the function ends
old_route_idx = content.find(old_route_start)
if old_route_idx != -1:
    new_logic = """class AdminReplyPayload(BaseModel):
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
        
        body = f"Hi there!\\n\\nAn admin has reviewed and replied to your recent feedback/report:\\n\\nYour Feedback: \\"{feedback_message}\\"\\n\\nAdmin Reply:\\n{reply_text}\\n\\nThanks for helping us improve MatDataHub!\\n\\nBest,\\nThe MatDataHub Engineering Team"
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
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
            
    return {"ok": True, "message": "Reply saved! (No user email found to notify)"}"""

    # We need to slice the content to replace the old function completely
    end_marker = 'return {"ok": True, "message": "Reply saved. No user email was found to notify."}'
    end_idx = content.find(end_marker) + len(end_marker)
    
    content = content[:old_route_idx] + new_logic + content[end_idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Backend logic updated to use BackgroundTasks.")
else:
    print("Could not find old backend logic.")
