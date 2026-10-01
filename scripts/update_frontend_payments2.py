import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\account\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = 'body: JSON.stringify({ tier })'
good = 'body: JSON.stringify({ tier, callback_url: window.location.href })'

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added callback_url to handleUpgrade in page.tsx")
else:
    print("Not found")
