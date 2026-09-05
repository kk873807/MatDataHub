import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_ui = 'st.text_input("API Key ID (Public)", value=data.get("api_key_id", ""), disabled=True)'
new_ui = 'st.markdown("### API Key ID (Public)")\n                            st.code(data.get("api_key_id", ""), language="text")'

content = content.replace(old_ui, new_ui)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated API Key ID UI to be copyable via st.code.")
