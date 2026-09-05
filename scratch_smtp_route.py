import sys

file_path = 'app/routers/admin.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_route = """@router.get("/test-smtp")
def test_smtp_connection(_: bool = Depends(verify_admin)):
    import smtplib
    import os
    sender_email = os.getenv("SMTP_EMAIL", "")
    sender_password = os.getenv("SMTP_PASSWORD", "")
    
    if not sender_password:
        return {"status": "error", "message": "SMTP_PASSWORD is empty or not loaded by the server."}
        
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.quit()
        return {"status": "success", "message": f"Successfully authenticated as {sender_email}!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
"""

if "/test-smtp" not in content:
    content += "\n" + new_route
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added /test-smtp to admin.py")
else:
    print("Route already exists.")
