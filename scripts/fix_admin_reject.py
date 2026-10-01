import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''@router.post("/contributions/{contrib_id}/reject")
def reject_contribution(contrib_id: int, db: Session = Depends(get_db), _: bool = Depends(verify_admin)):
    from app.models import CustomMaterial
    contrib = db.query(CustomMaterial).filter(CustomMaterial.id == contrib_id).first()
    if not contrib:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    contrib.status = "rejected"'''

good = '''@router.post("/contributions/{contrib_id}/reject")
def reject_contribution(contrib_id: int, db: Session = Depends(get_db), _: bool = Depends(verify_admin)):
    from app.models import CustomMaterial
    contrib = db.query(CustomMaterial).filter(CustomMaterial.id == contrib_id).first()
    if not contrib:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    if contrib.status == "approved":
        raise HTTPException(status_code=400, detail="Cannot reject a contribution that has already been approved and merged into the public database.")
    
    contrib.status = "rejected"'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed reject contribution")
else:
    print("Not found")
