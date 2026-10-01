path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\schemas.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = 'category: str = Field(..., max_length=100) = Field("General Feedback", max_length=50)'
good = 'category: str = Field("General Feedback", max_length=50)'
content = content.replace(bad, good)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Feedback schema fixed")
