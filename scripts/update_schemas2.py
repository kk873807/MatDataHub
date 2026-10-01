path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\schemas.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''class CustomMaterialResponse(CustomMaterialCreate):
    id: int
    user_id: int
    created_at: datetime
    class Config:'''

new_block = '''class CustomMaterialResponse(CustomMaterialCreate):
    id: int
    user_id: int
    status: str
    created_at: datetime
    class Config:'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added status to CustomMaterialResponse")
else:
    print("Block not found")
