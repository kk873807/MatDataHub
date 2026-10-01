import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bulk_pattern = re.compile(
    r'@router\.post\("/custom/bulk", response_model=dict\)\s*'
    r'def bulk_create_custom_materials\([\s\S]*?return \{"inserted": inserted\}'
)

new_bulk = '''@router.post("/custom/bulk", response_model=dict)
def bulk_create_custom_materials(
    materials: List[CustomMaterialCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    raise HTTPException(status_code=403, detail="Bulk upload is disabled. Only single material additions are permitted with source verification.")'''

content, num_subs = bulk_pattern.subn(new_bulk, content)
if num_subs > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("bulk patched!")
else:
    print("still not found")
