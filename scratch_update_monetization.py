import sys

file_path = 'app/routers/materials.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We need to add the daily limit logic and fix the current_user dependency
# First, insert the daily limit logic right after _check_mat_rate_limit
daily_limit_code = """
# --- Daily Lookup Limits (Monetization Strategy) ---
_daily_lookups = defaultdict(list)
FREE_DAILY_LIMIT = 50

def _check_daily_limit(request: Request, current_user: Optional[User]):
    # Pro and Advanced get unlimited lookups
    if current_user and current_user.tier in ["pro", "advanced"]:
        return

    # Track by user_id if logged in, otherwise by IP
    key = f"user_{current_user.id}" if current_user else f"ip_{_get_ip(request)}"
    now = time.time()
    
    timestamps = _daily_lookups[key]
    # Remove timestamps older than 24 hours (86400 seconds)
    timestamps[:] = [t for t in timestamps if now - t < 86400]
    
    if len(timestamps) >= FREE_DAILY_LIMIT:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS, 
            "You have reached your free limit of 50 material lookups for today. Upgrade to Pro for unlimited access!"
        )
    timestamps.append(now)
"""

content = content.replace("router = APIRouter(prefix=\"/materials\", tags=[\"Materials\"])", daily_limit_code + "\nrouter = APIRouter(prefix=\"/materials\", tags=[\"Materials\"])")

# Now change get_current_user to get_optional_user in the specific routes
content = content.replace("current_user: User = Depends(get_current_user),  # public", "current_user: Optional[User] = Depends(get_optional_user),  # public")
content = content.replace("current_user: User = Depends(get_current_user)", "current_user: Optional[User] = Depends(get_optional_user)")

# But wait, create_material and bulk_create_materials and find_similar_materials shouldn't be optional if they require auth.
# Actually find_similar_materials checks if not current_user: tier = "free". So it's fine.
# Let's fix get_material to actually use _check_daily_limit
content = re.sub(
    r'def get_material\((.*?)\):.*?material = db\.query\(Material\)',
    r'def get_material(\1):\n    _check_daily_limit(request, current_user)\n    material = db.query(Material)',
    content,
    flags=re.DOTALL
)
# We also need to add request: Request to get_material
content = content.replace('def get_material(\n    material_id: int,\n    db: Session = Depends(get_db),\n    current_user: Optional[User] = Depends(get_optional_user),  # public\n):', 'def get_material(\n    material_id: int,\n    request: Request,\n    db: Session = Depends(get_db),\n    current_user: Optional[User] = Depends(get_optional_user),  # public\n):')

# Write the new file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated materials.py with Monetization Daily Limits & Public Access.")
