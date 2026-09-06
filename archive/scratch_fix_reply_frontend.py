import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace frontend requests.post call for reply
old_frontend = """                                                resp = requests.post(
                                                    f"{API_BASE}/feedback/{c['id']}/reply", 
                                                    headers={"X-Admin-Secret": st.session_state.get("temp_admin_pw", ""), "X-Reply-Text": admin_msg}
                                                )"""

new_frontend = """                                                resp = requests.post(
                                                    f"{API_BASE}/feedback/{c['id']}/reply", 
                                                    headers={"X-Admin-Secret": st.session_state.get("temp_admin_pw", "")},
                                                    json={"reply_text": admin_msg}
                                                )"""

if old_frontend in content:
    content = content.replace(old_frontend, new_frontend)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Frontend reply route updated to use JSON payload.")
else:
    print("Could not find frontend route to replace.")
