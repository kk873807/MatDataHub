import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\feedback.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''def verify_admin(x_admin_secret: str = Header(...)):
    if not ADMIN_SECRET:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Admin access not configured.")
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid admin credentials.")
    return True'''

good = '''from app.routers.admin import verify_admin'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced verify_admin in feedback.py")
else:
    print("Could not find block")
