import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = '''    tier = req.tier.lower()
    if tier not in ["pro", "advanced"]:
        raise HTTPException(status_code=400, detail="Invalid tier.")'''

good_block = '''    tier = req.tier.lower()
    if tier not in ["pro", "advanced"]:
        raise HTTPException(status_code=400, detail="Invalid tier.")
        
    if current_user.tier == tier:
        raise HTTPException(status_code=400, detail=f"You are already on the {tier.capitalize()} tier.")
        
    if current_user.tier == "advanced" and tier == "pro":
        raise HTTPException(status_code=400, detail="You are currently on the Advanced tier. Downgrading to Pro requires contacting support.")'''

if bad_block in content:
    content = content.replace(bad_block, good_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added tier conflict checks")
else:
    print("Could not find tier block")
