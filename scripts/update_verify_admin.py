import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''def verify_admin(x_admin_secret: str = Header(...)):
    if not ADMIN_SECRET:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Admin access not configured.")
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid admin credentials.")
    return True'''

good = '''from app.auth import get_current_user

def verify_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Access denied. Admin privileges required.")
    return current_user'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated verify_admin in admin.py to use RBAC")
else:
    print("Could not find block")
