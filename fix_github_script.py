
import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\scripts\ingest_github_datasets.py'
content = open(path, 'r', encoding='utf-8').read()

# Replace troublesome unicode characters
content = content.replace('\u25b6', '>>')
content = content.replace('?', '-')
content = content.replace('—', '-')
content = content.replace('?', '>>')

open(path, 'w', encoding='utf-8').write(content)
print('Unicode fixed.')

