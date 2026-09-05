import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip_next_with_tab = False
unindent_mode = False
unindent_spaces = 4

for i, line in enumerate(lines):
    # Check for FAQ nested tab
    if "tab_faq, = st.tabs([" in line:
        continue # Skip this line
    if "with tab_faq:" in line and "tab_faq_main" not in line:
        unindent_mode = True
        continue # Skip this line
        
    # Check for Support nested tab
    if "tab_feedback, = st.tabs([" in line:
        continue # Skip this line
    if "with tab_feedback:" in line:
        unindent_mode = True
        continue # Skip this line

    # If we hit a new main tab, turn off unindent mode
    if unindent_mode and line.strip().startswith("with tab_") and line.strip().endswith(":"):
        unindent_mode = False

    if unindent_mode:
        if line.startswith("    "): # Only unindent if it actually has spaces
            new_lines.append(line[4:])
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Removed nested tabs successfully.")
