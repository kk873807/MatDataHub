path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\schemas.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'status: str' not in content:
    content = content.replace(
        'created_at: datetime',
        'created_at: datetime\n    status: str'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added status to schemas.py")
