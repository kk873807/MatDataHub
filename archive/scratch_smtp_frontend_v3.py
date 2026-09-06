import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '**💬 Recent Feedback**' in line or '**dY" Recent Feedback**' in line:
        # We found the spot
        insert_idx = i - 1
        break

code_to_insert = """
            # --- NEW SMTP DEBUGGER ---
            st.markdown("**🛠️ Server Diagnostics**")
            if st.button("🧪 Test SMTP Email Connection"):
                with st.spinner("Pinging Gmail SMTP..."):
                    smtp_res = requests.get(f"{API_BASE}/admin/test-smtp", headers={"X-Admin-Secret": active_pw})
                    if smtp_res.status_code == 200:
                        data = smtp_res.json()
                        if data.get("status") == "success":
                            st.success(data["message"])
                        else:
                            st.error(f"SMTP Server Error: {data['message']}")
                            st.info("HINT: If you are using Gmail, you cannot use your normal password. You MUST use a 16-letter 'App Password' generated from your Google Account Security settings.")
"""

lines.insert(insert_idx, code_to_insert)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Added SMTP button.")
