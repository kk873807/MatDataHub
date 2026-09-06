with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("scratch_lines_1944.txt", "w", encoding="utf-8") as out:
    for i in range(1935, 1955):
        if i < len(lines):
            out.write(f"{i+1}: {lines[i]}")
