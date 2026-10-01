import re
import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will append the two new endpoints to the end of the file.
new_endpoints = '''
@router.post("/contributions/{contrib_id}/approve")
def approve_contribution(contrib_id: int, db: Session = Depends(get_db), _: bool = Depends(verify_admin)):
    from app.models import CustomMaterial, Material
    contrib = db.query(CustomMaterial).filter(CustomMaterial.id == contrib_id).first()
    if not contrib:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    if contrib.status == "approved":
        raise HTTPException(status_code=400, detail="Already approved")

    # Move to public materials
    new_mat = Material(
        name=contrib.name,
        category=contrib.category,
        subcategory=contrib.subcategory,
        standard=contrib.grade,  # Mapping grade to standard for now, or keep grade? Public materials don't have grade, they have standard/origin
        origin="User Contributed",
        description=contrib.description,
        source_url=contrib.source_url,
        elastic_modulus=contrib.elastic_modulus,
        density=contrib.density,
        yield_strength_min=contrib.yield_strength_min,
        tensile_strength_min=contrib.tensile_strength_min
    )
    db.add(new_mat)
    contrib.status = "approved"
    db.commit()
    return {"message": "Contribution approved and added to public database"}

@router.post("/contributions/{contrib_id}/reject")
def reject_contribution(contrib_id: int, db: Session = Depends(get_db), _: bool = Depends(verify_admin)):
    from app.models import CustomMaterial
    contrib = db.query(CustomMaterial).filter(CustomMaterial.id == contrib_id).first()
    if not contrib:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    contrib.status = "rejected"
    db.commit()
    return {"message": "Contribution rejected"}
'''

if 'approve_contribution' not in content:
    content += new_endpoints
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added approve/reject endpoints")
else:
    print("Endpoints already exist")
