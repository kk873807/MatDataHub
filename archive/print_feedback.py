import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
text = "".join(lines[2750:2850])
text = text.encode("ascii", "ignore").decode()
print(text)
