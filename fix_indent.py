with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "    # --- THEME-AWARE CSS ---"
# Since it was unindented to 4 spaces, the end marker is now 4 spaces too
end_marker = '    """, unsafe_allow_html=True)\n'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx) + len(end_marker)

css_block = content[start_idx:end_idx]
content = content[:start_idx] + content[end_idx:]

# Find st.set_page_config
page_config_target = ")\n# --- APP STATE INITIALIZATION ---"
insert_idx = content.find(page_config_target) + len(")\n")

# Re-format css block to be 0 spaces indented
css_lines = css_block.split("\n")
clean_css_lines = []
for line in css_lines:
    if line.startswith("    "):
        clean_css_lines.append(line[4:])
    else:
        clean_css_lines.append(line)

clean_css = "\n".join(clean_css_lines)

content = content[:insert_idx] + "\n" + clean_css + "\n" + content[insert_idx:]

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("CSS moved to global scope and indentation fixed.")
