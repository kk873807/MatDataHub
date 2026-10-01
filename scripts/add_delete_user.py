import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

good = '''
@router.delete("/users/{user_id}")
def delete_user(user_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: completely delete a user account and their data."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    
    # Due to SQLAlchemy cascades/relationships (if configured), this will delete associated data.
    # If not fully cascaded, you might need to manually delete transactions, feedback, etc.
    db.delete(user)
    db.commit()
    return {"message": f"User {user.email} has been permanently deleted."}
'''

content = content.replace('    return {"message": f"User {user.email} blocked."}\n', '    return {"message": f"User {user.email} blocked."}\n' + good)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added delete_user endpoint")
