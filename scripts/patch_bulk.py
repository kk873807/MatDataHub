import sys

with open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
start_idx = content.find('@router.post("/custom/bulk", response_model=dict)')
if start_idx != -1:
    end_idx = content.find('return {"message": "Bulk import complete"', start_idx)
    end_idx = content.find('}', end_idx) + 1
    old_text = content[start_idx:end_idx]
    
    new_text = '''@router.post("/custom/bulk", response_model=dict)
def bulk_create_custom_materials(
    materials: List[CustomMaterialCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    raise HTTPException(status_code=403, detail="Bulk upload is disabled. Only single material additions are permitted with source verification.")'''
    
    content = content.replace(old_text, new_text)
    with open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Bulk endpoint patched successfully.")
else:
    print("Could not find bulk endpoint start.")
