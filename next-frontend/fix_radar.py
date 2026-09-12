import os
filepath = r'src\app\analytics\compare\page.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('stroke="#334155"', 'className="stroke-slate-200 dark:stroke-slate-700"')
text = text.replace('fill="#94a3b8"', 'className="fill-slate-600 dark:fill-slate-400"')
text = text.replace("style={{ mixBlendMode: 'screen' }}", 'className="mix-blend-multiply dark:mix-blend-screen opacity-70"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
