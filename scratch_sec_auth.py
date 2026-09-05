import sys
import re

file_path = 'app/auth.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update get_current_user to hash the incoming X-API-Key
old_api_check = """    api_key = request.headers.get("X-API-Key")
    if api_key:
        user = db.query(User).filter(User.api_key == api_key, User.is_active == True).first()"""

new_api_check = """    import hashlib
    api_key = request.headers.get("X-API-Key")
    if api_key:
        hashed_key = hashlib.sha256(api_key.encode('utf-8')).hexdigest()
        user = db.query(User).filter(User.api_key == hashed_key, User.is_active == True).first()"""

content = content.replace(old_api_check, new_api_check)

# Update get_optional_user to hash the incoming X-API-Key
old_api_check_opt = """    api_key = request.headers.get("X-API-Key")
    if api_key:
        user = db.query(User).filter(User.api_key == api_key, User.is_active == True).first()"""

content = content.replace(old_api_check_opt, new_api_check)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated auth.py with API Key Hashing.")
