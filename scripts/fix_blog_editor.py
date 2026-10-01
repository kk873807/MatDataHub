import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\BlogEditor.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad1 = '''export default function BlogEditor({ secret }: { secret: string }) {'''
good1 = '''export default function BlogEditor() {'''

bad2 = '''headers: { "Content-Type": "application/json", "X-Admin-Secret": secret },'''
good2 = '''headers: { "Content-Type": "application/json", "Authorization": `Bearer ${localStorage.getItem("token")}` },'''

if bad1 in content and bad2 in content:
    content = content.replace(bad1, good1).replace(bad2, good2)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed BlogEditor.tsx")
else:
    print("Could not find blocks in BlogEditor.tsx")
