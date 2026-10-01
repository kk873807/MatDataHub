import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''<MaterialManager secret={secret} />'''
good = '''<MaterialManager />'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed MaterialManager usage in page.tsx")
else:
    print("Could not find MaterialManager usage")
