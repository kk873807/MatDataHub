import sys

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_endpoint = '''
from app.models import CustomMaterial

@router.get("/user-contributions")
def get_all_user_contributions(_: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """
    Returns all user contributions grouped by user.
    """
    users = db.query(User).all()
    materials = db.query(CustomMaterial).all()
    
    user_map = {u.id: {"id": u.id, "name": u.name or "User", "email": u.email, "tier": u.tier} for u in users}
    
    contribs = {}
    for m in materials:
        if m.user_id not in contribs:
            contribs[m.user_id] = {
                "user": user_map.get(m.user_id, {"id": m.user_id, "name": "Unknown", "email": "unknown", "tier": "free"}),
                "materials": []
            }
        contribs[m.user_id]["materials"].append({
            "id": m.id,
            "name": m.name,
            "category": m.category,
            "source_url": m.source_url,
            "created_at": m.created_at
        })
        
    return list(contribs.values())
'''

if 'get_all_user_contributions' not in content:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(new_endpoint)
    print("Endpoint added to admin.py")
else:
    print("Endpoint already exists")
