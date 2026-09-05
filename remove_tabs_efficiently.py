import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Remove the sub-tab definitions
    if 'tab_faq, = st.tabs([' in line:
        continue
    if 'tab_feedback, = st.tabs([' in line:
        continue
        
    # Replace the with blocks
    if line.strip() == "with tab_faq:":
        new_lines.append(line.replace("with tab_faq:", "with tab_faq_main:"))
        continue
    if line.strip() == "with tab_feedback:":
        new_lines.append(line.replace("with tab_feedback:", "with tab_support_main:"))
        continue
        
    new_lines.append(line)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Removed child tabs efficiently!")
