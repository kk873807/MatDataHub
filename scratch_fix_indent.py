with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# We need to remove the empty `if user_tier in ("pro", "advanced"):` blocks
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip() == 'if user_tier in ("pro", "advanced"):':
        # Check if the next non-empty line is also 'if user_tier in ("pro", "advanced"):'
        j = i + 1
        is_duplicate = False
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and lines[j].strip() == 'if user_tier in ("pro", "advanced"):':
            # Skip this line and the empty lines
            i = j
            continue
    new_lines.append(line)
    i += 1

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Removed empty if blocks causing IndentationError.")
