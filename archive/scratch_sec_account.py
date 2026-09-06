import sys

file_path = 'app/routers/account.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update generate_api_key to hash the key before storing
old_gen = """    new_key = "mdh_" + secrets.token_hex(24)
    current_user.api_key = new_key
    db.commit()
    return {"ok": True, "api_key": new_key, "message": "New API Key generated successfully!"}"""

new_gen = """    import hashlib
    raw_key = "mdh_" + secrets.token_hex(24)
    hashed_key = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
    current_user.api_key = hashed_key
    db.commit()
    return {"ok": True, "api_key": raw_key, "message": "New API Key generated successfully! Store it safely, it will not be shown again."}"""

content = content.replace(old_gen, new_gen)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated account.py to store hashed API Keys.")
