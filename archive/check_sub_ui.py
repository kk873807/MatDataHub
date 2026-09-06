import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "st.info(\"\U0001f512 The Smart Substitution Engine is available on **Pro**" in line:
        for j in range(i-5, i+55):
            print(f"Line {j}: {lines[j].encode('ascii', 'backslashreplace').decode().strip()}")
        break
