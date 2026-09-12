import sys
with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div className="hidden md:flex items-center gap-3">' in line:
        lines[i+1] = '                      {userInfo?.is_admin && <Link href="/admin" className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" title="Admin"><ShieldAlert className="w-5 h-5" /></Link>}\\n'
        lines[i+2] = ''
        break

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)
