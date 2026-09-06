import sys

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the signature and auth logic
old_block = """@router.post("/{feedback_id}/reply")
def reply_to_feedback(
    feedback_id: int,
    request: Request,
    reply_text: str = Header(..., alias="X-Reply-Text"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"\"\"Admin endpoint to reply to user feedback and send an email notification.\"\"\"
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can reply to feedback.")"""

new_block = """@router.post("/{feedback_id}/reply")
def reply_to_feedback(
    feedback_id: int,
    request: Request,
    reply_text: str = Header(..., alias="X-Reply-Text"),
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    \"\"\"Admin endpoint to reply to user feedback and send an email notification.\"\"\""""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Backend logic fixed to use verify_admin.")
else:
    print("Could not find the block to replace in backend.")
