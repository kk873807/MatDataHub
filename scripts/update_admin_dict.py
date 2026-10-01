path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '"source_url": m.source_url,\n            "created_at": m.created_at'
new = '"source_url": m.source_url,\n            "status": getattr(m, "status", "pending"),\n            "created_at": m.created_at'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added status to admin.py dict")
else:
    print("Not found")
