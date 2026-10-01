import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_check = '''    existing_url = db.query(CustomMaterial).filter(CustomMaterial.source_url == str(mat.source_url)).first()
    if existing_url:
        raise HTTPException(status_code=400, detail="This Source URL has already been added to the database. Duplicate links are not permitted.")'''

good_check = '''    existing_url = db.query(CustomMaterial).filter(CustomMaterial.source_url == str(mat.source_url)).first()
    if existing_url:
        raise HTTPException(status_code=400, detail="This Source URL has already been submitted. Duplicate links are not permitted.")
    
    existing_main_url = db.query(Material).filter(Material.source_url == str(mat.source_url)).first()
    if existing_main_url:
        raise HTTPException(status_code=400, detail="This Source URL already exists in the main public database!")'''

if bad_check in content:
    content = content.replace(bad_check, good_check)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed duplicate url check")
else:
    print("Not found")
