import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
# Find 'with tab_home:'
start = -1
for i, line in enumerate(lines):
    if "with tab_home:" in line:
        start = i
        break

text = "".join(lines[start:start+50])
text = text.encode("ascii", "ignore").decode()
print(text)
