import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the broken injected code
bad_code_pattern = r'# --- API KEY SECTION ---.*?st\.markdown\("### 💎 Subscriptions & Upgrades"\)'
content = re.sub(bad_code_pattern, 'st.markdown("### 💎 Subscriptions & Upgrades")', content, flags=re.DOTALL)

# 2. Inject it into the correct Profile & Security tab
target = """            if account_menu == "🛡️ Profile & Security":
                st.markdown("### Profile Details")
                st.text_input("Full Name", value=user.get("name", ""))
                st.text_input("Email Address", value=user.get("email", ""), disabled=True)
                st.text_input("Authentication Provider", value=user.get("auth_provider", "email").title(), disabled=True)
                if st.button("Save Changes"):
                    st.success("Profile updated.")"""

new_ui = """
                st.divider()
                st.markdown("### 🔑 API Access")
                if user.get("tier") in ["pro", "advanced"]:
                    current_key = user.get("api_key")
                    if current_key:
                        st.code(current_key, language="text")
                        st.caption("Use this key in the `X-API-Key` header to authenticate programmatic requests.")
                    else:
                        st.info("You haven't generated an API Key yet.")
                    
                    if st.button("Generate New API Key"):
                        r = requests.post(
                            f"{API_BASE}/account/generate-api-key",
                            headers={"Authorization": f"Bearer {st.session_state.token}"}
                        )
                        if r.status_code == 200:
                            # Re-fetch user to get the new key
                            me_res = api_get("/auth/me")
                            if me_res["ok"]:
                                st.session_state.user = me_res["data"]
                            st.success("API Key generated!")
                            st.rerun()
                        else:
                            st.error("Failed to generate API Key.")
                else:
                    st.warning("API Access is only available on the Pro and Advanced tiers.")
                    if st.button("Upgrade to Pro to unlock API Access", type="primary"):
                        st.session_state.current_page = "pricing"
                        st.rerun()
"""

if target in content:
    content = content.replace(target, target + new_ui)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed API Key UI injection.")
else:
    print("Could not find target Profile & Security block.")
