import sys
with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(r'\n', '\n')

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
