
import os
path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\scripts\ingest_materials_project.py'
content = open(path, 'r', encoding='utf-8').read()
content = content.replace('?', '>>')
content = content.replace('?', '>>')
open(path, 'w', encoding='utf-8').write(content)
print('Fixed unicode in MP script')

