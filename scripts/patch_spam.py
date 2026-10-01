import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports safely
if 'from datetime import datetime, timedelta' not in content:
    content = content.replace('from fastapi import APIRouter', 'from fastapi import APIRouter\nfrom datetime import datetime, timedelta')

old_logic = '''    if not getattr(mat, 'source_url', None) or not str(mat.source_url).startswith('http'):
        raise HTTPException(status_code=400, detail="A valid source_url (http/https) is required.")'''

new_logic = '''    # --- Anti-Spam & Rate Limiting ---
    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
    recent_count = db.query(CustomMaterial).filter(
        CustomMaterial.user_id == current_user.id,
        CustomMaterial.created_at >= one_minute_ago
    ).count()
    if recent_count >= 5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait a minute before adding more materials.")

    one_day_ago = datetime.utcnow() - timedelta(days=1)
    daily_count = db.query(CustomMaterial).filter(
        CustomMaterial.user_id == current_user.id,
        CustomMaterial.created_at >= one_day_ago
    ).count()
    if daily_count >= 50:
        raise HTTPException(status_code=429, detail="Daily limit reached. You can only add up to 50 materials per 24 hours.")

    # --- Duplicate Prevention ---
    existing_name = db.query(CustomMaterial).filter(
        CustomMaterial.user_id == current_user.id,
        CustomMaterial.name.ilike(mat.name)
    ).first()
    if existing_name:
        raise HTTPException(status_code=400, detail=f"You have already added a material named '{mat.name}'.")

    existing_url = db.query(CustomMaterial).filter(CustomMaterial.source_url == str(mat.source_url)).first()
    if existing_url:
        raise HTTPException(status_code=400, detail="This Source URL has already been added to the database. Duplicate links are not permitted.")

    if not getattr(mat, 'source_url', None) or not str(mat.source_url).startswith('http'):
        raise HTTPException(status_code=400, detail="A valid source_url (http/https) is required.")'''

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Anti-spam and duplicate prevention added!")
else:
    print("Could not find insertion point.")
