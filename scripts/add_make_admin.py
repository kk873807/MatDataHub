import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\auth.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

good = '''@router.post("/make-me-admin")
def make_me_admin(
    x_admin_secret: str = Header(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    import os
    ADMIN_SECRET = os.getenv("ADMIN_SECRET")
    if not ADMIN_SECRET:
        raise HTTPException(status_code=500, detail="Server not configured with ADMIN_SECRET.")
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin secret.")
    
    current_user.is_admin = True
    db.commit()
    return {"message": f"{current_user.email} is now an admin."}
'''

if 'make_me_admin' not in content:
    content += "\n" + good
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added /make-me-admin endpoint")
else:
    print("make_me_admin already exists")
