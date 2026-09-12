import os
with open('src/app/blogs/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('import { API } from "@/lib/utils";', 'import { API } from "@/lib/api";')
with open('src/app/blogs/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed API import")
