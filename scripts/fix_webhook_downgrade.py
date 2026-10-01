import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.tier = tier
                    user.upgrade_status = None
                    user.requested_tier = None'''

good = '''                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    # Protect against unauthorized downgrades via webhook
                    if not (user.tier == "advanced" and tier == "pro"):
                        user.tier = tier
                        user.upgrade_status = None
                        user.requested_tier = None'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added webhook downgrade protection")
else:
    print("Could not find block")
