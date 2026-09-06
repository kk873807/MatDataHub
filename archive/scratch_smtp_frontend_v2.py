import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

smtp_button_code = """
            if active_pw:
                # --- NEW SMTP DEBUGGER ---
                st.subheader("🛠️ Server Diagnostics")
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

target = "if active_pw:"
if target in content and "Test SMTP Email Connection" not in content:
    content = content.replace(target, smtp_button_code, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added SMTP test button to frontend.")
else:
    print("Could not insert frontend button.")
