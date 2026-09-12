import os
import re

with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace any missing backticks in the className interpolation of the span
pattern = r'className=\{inline-flex items-center gap-1 px-2 py-0\.5 rounded-full text-\[10px\] font-bold uppercase tracking-wider border \$\{tierColor\}\}'
replacement = r'className={inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border }'

code = re.sub(pattern, replacement, code)

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Forced backticks via regex!")
