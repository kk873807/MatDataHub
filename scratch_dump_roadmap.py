with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(1670, 1700):
    print(lines[i].strip())
