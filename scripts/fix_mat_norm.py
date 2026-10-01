import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''    # --- Duplicate Prevention ---
    existing_name = db.query(CustomMaterial).filter(
        CustomMaterial.user_id == current_user.id,
        CustomMaterial.name.ilike(mat.name)
    ).first()'''

good = '''    # Normalize Inputs
    if mat.name: mat.name = mat.name.strip()
    if mat.source_url: mat.source_url = str(mat.source_url).strip().rstrip('/')

    # --- Duplicate Prevention ---
    existing_name = db.query(CustomMaterial).filter(
        CustomMaterial.user_id == current_user.id,
        CustomMaterial.name.ilike(mat.name)
    ).first()'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added input normalization")
else:
    print("Not found")
