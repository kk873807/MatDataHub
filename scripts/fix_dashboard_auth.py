p = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\dashboard\page.tsx'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

old = '.then(res => res.json())\n      .then(data => {\n        if (!data.detail) setProfile(data);\n      })'

new_code = (
    '.then(res => {\n'
    '        if (!res.ok) {\n'
    '          localStorage.removeItem("token");\n'
    '          window.location.href = "/?login=true";\n'
    '          return null;\n'
    '        }\n'
    '        return res.json();\n'
    '      })\n'
    '      .then(data => {\n'
    '        if (data && !data.detail) setProfile(data);\n'
    '      })\n'
    '      .catch(() => {\n'
    '        localStorage.removeItem("token");\n'
    '        window.location.href = "/?login=true";\n'
    '      })'
)

if old in content:
    content = content.replace(old, new_code)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: Dashboard auth fix applied (LF)')
else:
    old_crlf = old.replace('\n', '\r\n')
    new_crlf = new_code.replace('\n', '\r\n')
    if old_crlf in content:
        content = content.replace(old_crlf, new_crlf)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        print('SUCCESS: Dashboard auth fix applied (CRLF)')
    else:
        print('FAILED: Could not find target')
        lines = content.splitlines()
        for i in range(16, min(24, len(lines))):
            print(f'{i+1}: {repr(lines[i])}')
