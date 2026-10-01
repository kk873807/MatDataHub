import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = '''    if contrib.status == "approved":
        raise HTTPException(status_code=400, detail="Already approved")

    # Move to public materials'''

good_block = '''    if contrib.status == "approved":
        raise HTTPException(status_code=400, detail="Already approved")

    if contrib.source_url:
        existing = db.query(Material).filter(Material.source_url == contrib.source_url).first()
        if existing:
            raise HTTPException(status_code=400, detail="This source URL already exists in the public database! Please Reject this contribution instead.")

    # Move to public materials'''

if bad_block in content:
    content = content.replace(bad_block, good_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added approval duplicate check")
else:
    print("Block not found")
