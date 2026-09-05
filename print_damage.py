import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
# Let's extract line 735 to 810 to see what happened and what the end marker is
text = "".join(lines[735:810])
text = text.encode("ascii", "ignore").decode()
print(text)
