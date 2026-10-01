import os

file_path = 'app/routers/materials.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

menu_endpoint = """
@router.get("/menu", response_model=List[MaterialMenuResponse])
@limiter.limit("60/minute")
def get_material_menu(request: Request, db: Session = Depends(get_db)):
    \"\"\"Returns only ID and Name for frontend dropdowns to prevent bulk data scraping.\"\"\"
    results = db.query(Material.id, Material.name).order_by(Material.name).all()
    return [{"id": r.id, "name": r.name} for r in results]
"""

content = content.replace('from app.schemas import (', 'from app.schemas import (\n    MaterialMenuResponse,')
content = content.replace('@router.get("/autocomplete")', menu_endpoint + '\n@router.get("/autocomplete")')
content = content.replace('per_page: int = Query(20, ge=1, le=2000', 'per_page: int = Query(20, ge=1, le=50')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
