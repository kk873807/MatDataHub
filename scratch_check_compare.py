with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "TAB 2: COMPARE MATERIALS" in line:
        for j in range(i, i+50):
            print(lines[j].strip())
        break
