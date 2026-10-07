import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old = 'mat_name_lower = str(mat_name).lower() if mat_name else ""'
new = 'mat_name_lower = str(raw_name).lower() if raw_name else ""'
if old in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))
    print('Replaced')
else:
    print('Not found')
