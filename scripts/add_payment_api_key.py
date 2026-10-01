import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if 'generate_api_credentials' not in content:
    content = content.replace('from app.auth import get_current_user', 'from app.auth import get_current_user, generate_api_credentials')

# Add API generation logic
bad = '''                        user.tier = tier
                        user.upgrade_status = None
                        user.requested_tier = None'''

good = '''                        user.tier = tier
                        user.upgrade_status = None
                        user.requested_tier = None
                        
                        # Generate API credentials for Advanced users if they don't have them
                        if tier == "advanced" and not user.api_key:
                            raw_key, raw_secret = generate_api_credentials()
                            user.api_key = raw_key
                            user.api_secret = raw_secret'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added API key generation to payments.py webhook")
else:
    print("Could not find block")
