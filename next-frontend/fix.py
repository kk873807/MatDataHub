import sys
with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

target = '                    <div className="hidden md:flex items-center gap-3">\\n                      \\n\\n                    </div>'
replacement = '                    <div className="hidden md:flex items-center gap-3">\\n                      {userInfo?.is_admin && <Link href="/admin" className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" title="Admin"><ShieldAlert className="w-5 h-5" /></Link>}\\n                    </div>'

code = code.replace(target, replacement)
target_win = '                    <div className="hidden md:flex items-center gap-3">\\r\\n                      \\r\\n\\r\\n                    </div>'
replacement_win = '                    <div className="hidden md:flex items-center gap-3">\\r\\n                      {userInfo?.is_admin && <Link href="/admin" className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" title="Admin"><ShieldAlert className="w-5 h-5" /></Link>}\\r\\n                    </div>'
code = code.replace(target_win, replacement_win)

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
