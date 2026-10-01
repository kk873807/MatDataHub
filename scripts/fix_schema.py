path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\schemas.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = 'source_url: str = Field(..., max_length=1000) = Field(..., max_length=500, description="Source URL is required for verified tracking")'
good = 'source_url: str = Field(..., max_length=500, description="Source URL is required for verified tracking")'

content = content.replace(bad, good)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Schemas fixed")
