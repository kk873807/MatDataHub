import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "st.tabs([" in line:
        print(f"Line {i}: {line.strip()}")
