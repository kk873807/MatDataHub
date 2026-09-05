import sys
import re

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the reply_to_feedback signature
old_route = """@router.post("/{feedback_id}/reply")
def reply_to_feedback(
    feedback_id: int,
    request: Request,
    reply_text: str = Header(..., alias="X-Reply-Text"),
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):"""

new_route = """from pydantic import BaseModel
class AdminReplyPayload(BaseModel):
    reply_text: str

@router.post("/{feedback_id}/reply")
def reply_to_feedback(
    feedback_id: int,
    payload: AdminReplyPayload,
    request: Request,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    reply_text = payload.reply_text"""

if old_route in content:
    content = content.replace(old_route, new_route)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Backend reply route updated to use JSON payload instead of Header.")
else:
    print("Could not find backend route to replace.")
