import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add `import requests` at the top if it doesn't exist
if 'import requests' not in content:
    content = content.replace('from fastapi import APIRouter', 'import requests\nfrom fastapi import APIRouter', 1)

# 2. Patch create_custom_material
old_custom = '''@router.post("/custom", response_model=CustomMaterialResponse)
def create_custom_material(
    mat: CustomMaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.tier != "advanced" and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Custom Materials are exclusively available on the Advanced tier.")
    
    db_mat = CustomMaterial(**mat.model_dump(), user_id=current_user.id)
    db.add(db_mat)
    db.commit()
    db.refresh(db_mat)
    return db_mat'''

new_custom = '''@router.post("/custom", response_model=CustomMaterialResponse)
def create_custom_material(
    mat: CustomMaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.tier != "advanced" and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Custom Materials are exclusively available on the Advanced tier.")
    
    if not getattr(mat, 'source_url', None) or not str(mat.source_url).startswith('http'):
        raise HTTPException(status_code=400, detail="A valid source_url (http/https) is required.")
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(mat.source_url, headers=headers, timeout=10, allow_redirects=True, stream=True)
        r.close()
        if r.status_code >= 400 and r.status_code not in [403, 429]:
            raise HTTPException(status_code=400, detail=f"Source URL verification failed (HTTP {r.status_code}). Please provide a valid and authentic primary source link.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail="Source URL verification failed. The link is unreachable or invalid.")
    
    db_mat = CustomMaterial(**mat.model_dump(), user_id=current_user.id)
    db.add(db_mat)
    db.commit()
    db.refresh(db_mat)
    return db_mat'''

# Handle both \n and \r\n
if old_custom in content:
    content = content.replace(old_custom, new_custom)
elif old_custom.replace('\n', '\r\n') in content:
    content = content.replace(old_custom.replace('\n', '\r\n'), new_custom.replace('\n', '\r\n'))
else:
    print("Could not find create_custom_material")

# 3. Patch bulk_create_custom_materials
# Let's use regex for this to be safer against slight differences.
bulk_pattern = re.compile(
    r'@router\.post\("/custom/bulk", response_model=dict\)\s*'
    r'def bulk_create_custom_materials\([\s\S]*?return \{"message": "Bulk import complete", "inserted": inserted, "skipped": skipped\}'
)

new_bulk = '''@router.post("/custom/bulk", response_model=dict)
def bulk_create_custom_materials(
    materials: List[CustomMaterialCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    raise HTTPException(status_code=403, detail="Bulk upload is disabled. Only single material additions are permitted with source verification.")'''

content, num_subs = bulk_pattern.subn(new_bulk, content)
if num_subs == 0:
    print("Could not find bulk_create_custom_materials")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("materials.py patched successfully!")
