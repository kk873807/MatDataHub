import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('  return (\n    <main className="flex flex-col p-6 lg:p-10 w-full min-h-screen">')
if idx != -1:
    with open('admin_ui_bottom_fixed.txt', 'w', encoding='utf-8') as f2:
        f2.write(content[idx:])
    print("Found correct bottom half")
else:
    print("Could not find bottom half")
