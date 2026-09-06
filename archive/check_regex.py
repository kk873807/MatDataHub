import sys
import re
with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()
if "r'title:\s*\"(.*?)\"'" in content or "r'title:\\s*\"(.*?)\"'" in content:
    print("Regex is intact")
else:
    print("Regex is broken")
    
# Let's print the actual line to be sure
for i, line in enumerate(content.split("\n")):
    if "t_match = " in line:
        print(line)
