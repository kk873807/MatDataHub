with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "tab_home, tab_guide, tab_browse" in line and "st.tabs" in line:
        # We find the definition line
        lines[i] = line.replace("tab_faq, tab_feedback = st.tabs([", "tab_faq, tab_feedback, tab_substitute, tab_enterprise = st.tabs([")
    if "dY' Help & Contact" in line and "Home" in line:
        lines[i] = line.replace("\"dY' Help & Contact\"", "\"dY' Help & Contact\", \"?? Smart Substitute (PRO)\", \"?? Enterprise BOM (ADV)\"")

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Tabs updated.")
