with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(1935, 1955):
    if i < len(lines):
        print(f"{i+1}: {repr(lines[i])}")
