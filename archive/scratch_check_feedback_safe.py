with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("out_feedback_safe.txt", "w", encoding="utf-8") as out:
    for i, line in enumerate(lines):
        if "TAB: FEEDBACK" in line:
            for j in range(i, i+80):
                if j < len(lines):
                    out.write(lines[j])
            break
