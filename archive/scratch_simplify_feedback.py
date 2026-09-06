import sys
import re

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the class AdminReplyPayload and replace everything until the end of the file
# since it is the last route in the file.
start_idx = content.find("class AdminReplyPayload(BaseModel):")
if start_idx != -1:
    new_route = """class AdminReplyPayload(BaseModel):
    reply_text: str

@router.post("/{feedback_id}/reply")
def reply_to_feedback(
    feedback_id: int,
    payload: AdminReplyPayload,
    request: Request,
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
            
    return {"ok": True, "message": "Official Reply pinned to thread successfully!"}
"""
    content = content[:start_idx] + new_route
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Simplified feedback reply route.")
else:
    print("Could not find start index in feedback.py.")
