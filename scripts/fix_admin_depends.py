import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = "def get_all_transactions(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):"
good = "def get_all_transactions(db: Session = Depends(get_db), _: bool = Depends(verify_admin)):"

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed Depends in admin.py")
else:
    print("Could not find line")
