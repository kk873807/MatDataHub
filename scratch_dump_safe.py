with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("out_safe.txt", "w", encoding="utf-8") as out:
    for i in range(1670, 1720):
        out.write(f"{i}: {lines[i]}")
