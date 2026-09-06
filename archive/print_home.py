import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
text = "".join(lines[1180:1280])
text = text.encode("ascii", "ignore").decode()
print(text)
