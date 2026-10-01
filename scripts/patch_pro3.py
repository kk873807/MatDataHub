import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_post = '''    if current_user.tier != "advanced" and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Custom Materials are exclusively available on the Advanced tier.")'''
new_post = '''    if current_user.tier not in ["advanced", "pro"] and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Custom Materials are exclusively available on the Pro and Advanced tiers.")'''

old_get = '''    if current_user.tier != "advanced" and not current_user.is_admin:
        return []'''
new_get = '''    if current_user.tier not in ["advanced", "pro"] and not current_user.is_admin:
        return []'''

content = content.replace(old_post, new_post)
content = content.replace(old_get, new_get)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Materials router patched for PRO")
