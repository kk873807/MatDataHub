import os

with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "alert('Keyboard shortcuts:" in line:
        lines[i] = "                        <button onClick={() => alert('Keyboard shortcuts: \\nCtrl+K: Search\\nCtrl+/: Shortcuts')} className=\"w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors text-left\">\n"
        print(f"Replaced line {i}")
    elif 'className="w-full flex items-center gap-2 px-3 py-2 text-sm' in line and "Keyboard shortcuts:" not in line and "Keyboard Shortcuts" not in line and "Sign Out" not in line:
        lines[i] = ""

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.writelines([l for l in lines if l.strip() != ""])

print("Fixed alert newline!")
