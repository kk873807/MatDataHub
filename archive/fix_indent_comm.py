import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_community = False
for line in lines:
    if line.strip() == "with tab_community:":
        in_community = True
        new_lines.append(line)
        continue
        
    if in_community:
        if line.strip() == "with tab_feedback:":
            in_community = False
            new_lines.append(line)
            continue
            
        # Fix indentation: remove leading spaces and add exactly 8 spaces
        if line.strip() == "":
            new_lines.append("\n")
        else:
            new_lines.append("        " + line.strip() + "\n")
    else:
        new_lines.append(line)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Indentation fixed.")
