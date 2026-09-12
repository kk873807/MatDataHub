import os

with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

bad_string = 'className={inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border }'
good_string = 'className={inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border }'

code = code.replace(bad_string, good_string)

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed broken variable expansion!")
