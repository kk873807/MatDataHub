import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if '# --- API KEY SECTION ---' in line:
        skip = True
    if skip and 'st.error("Failed to generate API Key.")' in line:
        skip = False
        continue
    if not skip:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Removed bad API key block.")
