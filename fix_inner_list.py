with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "tab_home, tab_guide, tab_browse" in line and "st.tabs" in line:
        pass # Already updated
    if "Help & Contact" in line and "FAQ" in line and "Home" in line:
        # Just rewrite the line entirely because encoding is a mess
        lines[i] = '        "🏠 Home", "📖 Platform Guide", "🔍 Database", "⚖️ Compare", "⚙️ Engineering (BOM)", "🤖 AI Advisor", "❓ FAQ", "🎫 Help & Contact", "🔄 Smart Substitute (PRO)", "📊 Enterprise BOM (ADV)"\n'

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Inner list updated.")
