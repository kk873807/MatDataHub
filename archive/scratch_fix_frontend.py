import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_headers = 'headers={"Authorization": f"Bearer {st.session_state.token}", "X-Reply-Text": admin_msg}'
new_headers = 'headers={"X-Admin-Secret": st.session_state.get("temp_admin_pw", ""), "X-Reply-Text": admin_msg}'

if old_headers in content:
    content = content.replace(old_headers, new_headers)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Frontend headers fixed.")
else:
    print("Could not find frontend headers to replace.")
