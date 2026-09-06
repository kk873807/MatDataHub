import sys

file_path = 'app/routers/account.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_gen = """    import hashlib
    raw_key = "mdh_" + secrets.token_hex(24)
    hashed_key = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
    current_user.api_key = hashed_key
    db.commit()
    return {"ok": True, "api_key": raw_key, "message": "New API Key generated successfully! Store it safely, it will not be shown again."}"""

new_gen = """    import hashlib
    import base64
    # Generate an API Key ID and a Secret
    key_id = "mdh_key_" + secrets.token_hex(8)
    raw_secret = "mdh_secret_" + secrets.token_hex(24)
    
    # We only store the hash of the secret for authentication.
    hashed_secret = hashlib.sha256(raw_secret.encode('utf-8')).hexdigest()
    current_user.api_key = hashed_secret
    db.commit()
    
    return {
        "ok": True, 
        "api_key_id": key_id,
        "api_secret": raw_secret,
        "message": "API Key generated successfully!"
    }"""

content = content.replace(old_gen, new_gen)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated account.py to return key_id and secret")
