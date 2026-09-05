import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
# Find 'with st.sidebar:'
start = -1
for i, line in enumerate(lines):
    if "with st.sidebar:" in line:
        start = i
        break

if start != -1:
    text = "".join(lines[start:start+100])
    text = text.encode("ascii", "ignore").decode()
    print(text)
