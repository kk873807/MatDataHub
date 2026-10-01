path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\schemas.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_name = 'name: str = Field(..., max_length=255) = Field(..., min_length=1, max_length=200, examples=["AISI 304 Stainless Steel"])'
good_name = 'name: str = Field(..., min_length=1, max_length=200, examples=["AISI 304 Stainless Steel"])'
content = content.replace(bad_name, good_name)

bad_category = 'category: str = Field(..., max_length=100) = Field(..., min_length=1, max_length=100, examples=["Metal"])'
good_category = 'category: str = Field(..., min_length=1, max_length=100, examples=["Metal"])'
content = content.replace(bad_category, good_category)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Schemas syntax fixed")
