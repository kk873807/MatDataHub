import os

file_path = 'app/routers/materials.py'

content = """
# ──────────────────────────────────────────────
# POST /materials/{material_id}/save
# ──────────────────────────────────────────────
@router.post("/{material_id}/save")
def toggle_save_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models import SavedMaterial, Material
    mat = db.query(Material).filter(Material.id == material_id).first()
    if not mat:
        raise HTTPException(status_code=404, detail="Material not found")
        
    existing = db.query(SavedMaterial).filter(SavedMaterial.user_id == current_user.id, SavedMaterial.material_id == material_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {"status": "unsaved", "material_id": material_id}
    else:
        new_save = SavedMaterial(user_id=current_user.id, material_id=material_id)
        db.add(new_save)
        db.commit()
        return {"status": "saved", "material_id": material_id}
        
# ──────────────────────────────────────────────
# GET /materials/me/saved
# ──────────────────────────────────────────────
@router.get("/me/saved", response_model=List[MaterialOut])
def get_saved_materials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models import SavedMaterial, Material
    saved = db.query(SavedMaterial).filter(SavedMaterial.user_id == current_user.id).all()
    if not saved:
        return []
    
    mat_ids = [s.material_id for s in saved]
    materials = db.query(Material).filter(Material.id.in_(mat_ids)).offset(skip).limit(limit).all()
    return materials
"""

with open(file_path, 'a', encoding='utf-8') as f:
    f.write(content)
