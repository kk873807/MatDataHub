import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '499<span className="text-lg' in line:
        lines[i] = '              <div className="text-4xl font-extrabold text-white mb-8">₹499<span className="text-lg font-medium text-slate-500">/mo</span></div>\n'
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
    print("Fixed accurately")
