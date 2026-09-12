import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\account\page.tsx'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('  if (!profile) return (')
if start_idx != -1:
    end_idx = text.find('  return (\n    <main className="flex flex-col', start_idx)
    if end_idx != -1:
        text = text[:start_idx] + text[end_idx:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("Removed split auth screen from account page.")
    else:
        print("Could not find end of split auth screen.")
else:
    print("Could not find start of split auth screen.")
