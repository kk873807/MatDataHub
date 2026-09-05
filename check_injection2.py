import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
# Check lines right before with tab_browse_main:
idx = -1
for i, line in enumerate(lines):
    if "with tab_browse_main:" in line:
        idx = i
        break

if idx != -1:
    text = "".join(lines[idx-30:idx+2])
    print(text.encode("ascii", "backslashreplace").decode())
