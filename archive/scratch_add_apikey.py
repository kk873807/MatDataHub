import sys

file_path = 'app/routers/account.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

new_route = """
import secrets

@router.post("/generate-api-key")
def generate_api_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.tier not in ["pro", "advanced"]:
        raise HTTPException(status_code=403, detail="API Keys are only available for Pro and Advanced tiers.")
        
    new_key = "mdh_" + secrets.token_hex(24)
    current_user.api_key = new_key
    db.commit()
    return {"ok": True, "api_key": new_key, "message": "New API Key generated successfully!"}
"""

if "generate-api-key" not in content:
    content = content + "\n" + new_route
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added generate-api-key route.")
else:
    print("Route already exists.")
