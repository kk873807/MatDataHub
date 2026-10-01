path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AdvancedMaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Regex to cleanly strip it
content = re.sub(
    r'<div className="mt-6 text-center text-slate-500 dark:text-slate-400">\s*<a href="/Admin_Material_Upload_Guide\.pdf"[^>]*>\s*View Admin Upload Guide \(PDF\)\s*</a>\s*</div>',
    '',
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed link")
