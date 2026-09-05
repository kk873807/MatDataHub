import sys
import re

file_path = 'app/auth.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add X-API-Key checking to get_current_user
old_func = """def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:"""

new_func = """from fastapi import Request

def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    # 1. Check for API Key first (for ERP/Programmatic access)
    api_key = request.headers.get("X-API-Key")
    if api_key:
        user = db.query(User).filter(User.api_key == api_key, User.is_active == True).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API Key.")
        if getattr(user, 'is_blocked', False):
            raise HTTPException(status_code=403, detail="Account is blocked.")
        return user
"""

# Wait, get_current_user has the logic inside it already, I need to replace it carefully.
content = re.sub(
    r'def get_current_user\(\n.*?\) -> User:.*?if credentials is None:',
    r'def get_current_user(\n    request: Request,\n    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),\n    db: Session = Depends(get_db),\n) -> User:\n    api_key = request.headers.get("X-API-Key")\n    if api_key:\n        user = db.query(User).filter(User.api_key == api_key, User.is_active == True).first()\n        if not user:\n            raise HTTPException(status_code=401, detail="Invalid API Key")\n        if getattr(user, "is_blocked", False):\n            raise HTTPException(status_code=403, detail="Account blocked.")\n        return user\n\n    if credentials is None:',
    content,
    flags=re.DOTALL
)

# And do the same for get_optional_user
content = re.sub(
    r'def get_optional_user\(\n.*?\) -> Optional\[User\]:.*?if credentials is None:',
    r'def get_optional_user(\n    request: Request,\n    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),\n    db: Session = Depends(get_db),\n) -> Optional[User]:\n    api_key = request.headers.get("X-API-Key")\n    if api_key:\n        user = db.query(User).filter(User.api_key == api_key, User.is_active == True).first()\n        if user and not getattr(user, "is_blocked", False):\n            return user\n\n    if credentials is None:',
    content,
    flags=re.DOTALL
)

# Also ensure Request is imported at the top of auth.py if not already
if "from fastapi import Request" not in content and "from fastapi import" in content:
    content = content.replace("from fastapi import", "from fastapi import Request,", 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated get_current_user to support X-API-Key.")
