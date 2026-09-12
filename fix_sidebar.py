import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\Sidebar.tsx'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "if (pathname === '/') return null;" in line:
        continue
    if "return (" in line and "<aside" in "".join(lines):
        # We will insert just before return (
        new_lines.append("  if (pathname === '/') return null;\n")
        new_lines.append(line)
        # to ensure it only inserts once:
        # Actually just a simple hack, I will do it safer:
        break
    else:
        new_lines.append(line)

# Let's do it by reading the whole file to make sure it's accurate
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove any existing early returns
text = text.replace("  if (pathname === '/') return null;\n", "")
text = text.replace("  if (pathname === '/') return null;", "")

# Add it exactly before return (
target = "  return (\n    <aside"
replacement = "  if (pathname === '/') return null;\n  return (\n    <aside"

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully")
else:
    print("Target not found")

