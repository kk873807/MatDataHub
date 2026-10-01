path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\schemas.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add max lengths
content = content.replace('name: str', 'name: str = Field(..., max_length=255)')
content = content.replace('category: str', 'category: str = Field(..., max_length=100)')
content = content.replace('description: Optional[str] = None', 'description: Optional[str] = Field(None, max_length=5000)')
content = content.replace('subcategory: Optional[str] = None', 'subcategory: Optional[str] = Field(None, max_length=100)')
content = content.replace('grade: Optional[str] = None', 'grade: Optional[str] = Field(None, max_length=100)')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Schemas constraints added")
