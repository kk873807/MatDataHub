import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\schemas.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_schema = '''class CustomMaterialCreate(BaseModel):
    name: str = Field(..., max_length=255)
    category: str = Field(..., max_length=100)
    source_url: str = Field(..., max_length=1000)'''

good_schema = '''class CustomMaterialCreate(BaseModel):
    name: str = Field(..., max_length=200)
    category: str = Field(..., max_length=50)
    source_url: str = Field(..., max_length=500)'''

if bad_schema in content:
    content = content.replace(bad_schema, good_schema)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed CustomMaterialCreate bounds")
else:
    print("Not found")
