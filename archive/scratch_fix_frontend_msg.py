import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_frontend_logic = """                                                if resp.status_code == 200:
                                                    st.session_state[f"show_admin_reply_{c['id']}"] = False
                                                    st.success("Official reply posted and email dispatched!")
                                                    st.rerun()"""

new_frontend_logic = """                                                if resp.status_code == 200:
                                                    st.session_state[f"show_admin_reply_{c['id']}"] = False
                                                    data = resp.json()
                                                    msg = data.get("message", "Official reply posted!")
                                                    st.success(msg)
                                                    import time
                                                    time.sleep(2)
                                                    st.rerun()"""

if old_frontend_logic in content:
    content = content.replace(old_frontend_logic, new_frontend_logic)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Frontend updated to display the exact backend message.")
else:
    print("Could not find frontend logic to replace.")
