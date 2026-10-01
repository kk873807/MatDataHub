import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''            "notes": {
                "user_id": str(current_user.id),
                "tier": tier
            }
        }
        
        if req.callback_url:'''

good = '''            "notes": {
                "user_id": str(current_user.id),
                "tier": tier
            },
            "options": {
                "checkout": {
                    "name": "MatDataHub"
                }
            }
        }
        
        if req.callback_url:'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added options.checkout.name = MatDataHub")
else:
    print("Could not find block")
