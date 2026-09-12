import os

with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'className={inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border }', 
    'className={inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border }'
)

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed backticks!")
