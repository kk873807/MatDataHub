with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("scratch_lines_compare.txt", "w", encoding="utf-8") as out:
    for i, line in enumerate(lines):
        if "TAB 2: COMPARE MATERIALS" in line:
            for j in range(i, i+50):
                out.write(lines[j])
            break
