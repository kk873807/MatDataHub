import os
filepath = r'src\app\materials\page.tsx'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<Link href={/materials/} className=\"font-bold', '<Link href={/materials/} className=\"font-bold')
text = text.replace('<Link href={/materials/} className=\"inline-flex', '<Link href={/materials/} className=\"inline-flex')

text = text.replace('style={{ width: {Math.min(((mat.yield_strength_min || 0) / 1000) * 100, 100)}% }}', 'style={{ width: ${Math.min(((mat.yield_strength_min || 0) / 1000) * 100, 100)}% }}')
text = text.replace('style={{ width: {Math.min(((mat.density || 0) / 20) * 100, 100)}% }}', 'style={{ width: ${Math.min(((mat.density || 0) / 20) * 100, 100)}% }}')

bad_span = '<span className={inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold }>'
good_span = '<span className={inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold }>'
text = text.replace(bad_span, good_span)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
