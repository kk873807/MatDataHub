import sys

with open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''@router.post("/custom", response_model=CustomMaterialResponse)
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

new_func = '''import requests

@router.post("/custom", response_model=CustomMaterialResponse)
def create_custom_material(
    mat: CustomMaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.tier != "advanced" and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Custom Materials are exclusively available on the Advanced tier.")
    
    if not mat.source_url or not mat.source_url.startswith('http'):
        raise HTTPException(status_code=400, detail="A valid source_url (http/https) is required.")
        
    try:
        # Verify if the source is live/authentic
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        # Use a quick GET request to verify the link
        r = requests.get(mat.source_url, headers=headers, timeout=10, allow_redirects=True, stream=True)
        r.close()
        if r.status_code >= 400 and r.status_code not in [403, 429]: # 403/429 are usually bot blocks, not dead links
            raise HTTPException(status_code=400, detail=f"Source URL verification failed (HTTP {r.status_code}). Please provide a valid and authentic primary source link.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail="Source URL verification failed. The link is unreachable or invalid.")
    
    db_mat = CustomMaterial(**mat.model_dump(), user_id=current_user.id)
    db.add(db_mat)
    db.commit()
    db.refresh(db_mat)
    return db_mat'''

if old_func in content:
    content = content.replace(old_func, new_func)
elif old_func.replace('\n', '\r\n') in content:
    content = content.replace(old_func.replace('\n', '\r\n'), new_func.replace('\n', '\r\n'))
else:
    print('Failed to find create_custom_material')

old_bulk = '''@router.post("/custom/bulk", response_model=dict)
def bulk_create_custom_materials(
    materials: List[CustomMaterialCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.tier != "advanced" and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Custom Materials are exclusively available on the Advanced tier.")
    
    inserted = 0
    skipped = 0
    for m in materials:
        # Check if exists for this user
        existing = db.query(CustomMaterial).filter(
            CustomMaterial.name == m.name,
            CustomMaterial.user_id == current_user.id
        ).first()
        if existing:
            skipped += 1
            continue
            
        db_mat = CustomMaterial(**m.model_dump(), user_id=current_user.id)
        db.add(db_mat)
        inserted += 1
        
    db.commit()
    return {"message": "Bulk import complete", "inserted": inserted, "skipped": skipped}'''

new_bulk = '''@router.post("/custom/bulk", response_model=dict)
def bulk_create_custom_materials(
    materials: List[CustomMaterialCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    raise HTTPException(status_code=403, detail="Bulk upload is disabled. Only single material additions are permitted with source verification.")'''

if old_bulk in content:
    content = content.replace(old_bulk, new_bulk)
elif old_bulk.replace('\n', '\r\n') in content:
    content = content.replace(old_bulk.replace('\n', '\r\n'), new_bulk.replace('\n', '\r\n'))
else:
    print('Failed to find bulk_create_custom_materials')

with open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('materials.py updated')
