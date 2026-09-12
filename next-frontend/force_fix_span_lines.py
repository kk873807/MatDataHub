import os

with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'className={`inline-flex items-center gap-1' in line or 'className={inline-flex items-center gap-1' in line:
        lines[i] = '                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${tierColor}`}>\n'
        print(f"Replaced line {i}")

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed line by iteration without powershell string interpolation!")
