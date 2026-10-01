import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''        if req.callback_url:
            payment_link_data["callback_url"] = req.callback_url
            payment_link_data["callback_method"] = "get"'''

good = '''        if req.callback_url:
            if not req.callback_url.startswith(("http://", "https://")):
                raise HTTPException(status_code=400, detail="Invalid callback URL.")
            payment_link_data["callback_url"] = req.callback_url
            payment_link_data["callback_method"] = "get"'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added callback_url protocol validation")
else:
    print("Could not find block")
