import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Let's completely clean up the duplicated injections around 1900
new_lines = []
skip = False
for i, line in enumerate(lines):
    # Fix the Custom Materials menu if we accidentally duplicated it
    if "Custom Materials (Enterprise)" in line and "st.radio" not in line and "elif account_menu" not in line and "###" not in line and "Upload your" not in line:
        pass # keep it
        
with open("scratch_dump.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
