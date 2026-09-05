import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "st.subheader(\"Side-by-Side Material Comparison\")" in line:
        print(f"Line {i}")
