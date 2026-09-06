import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
# Find 'with tab_guide:'
start = -1
for i, line in enumerate(lines):
    if "with tab_guide:" in line:
        start = i
        break
        
end = -1
for i in range(start + 1, len(lines)):
    if "with tab_browse_main:" in lines[i]:
        end = i
        break

text = "".join(lines[start:end])
text = text.encode("ascii", "ignore").decode()
print(text)
