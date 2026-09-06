import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1900, 1940):
    if i < len(lines):
        print(f"{i}: {lines[i].strip()}")
