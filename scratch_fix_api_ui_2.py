import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the broken injected code
bad_code_pattern = r'# --- API KEY SECTION ---.*?st\.markdown\("### 💎 Subscriptions & Upgrades"\)'
content = re.sub(bad_code_pattern, 'st.markdown("### 💎 Subscriptions & Upgrades")', content, flags=re.DOTALL)

# Find the Profile Details section
pattern = r'(st\.markdown\("### Profile Details"\)\n.*?\n                if st\.button\("Save Changes"\):\n                    st\.success\("Profile updated\."\))'

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
                        import requests
                        r = requests.post(
                            f"{API_BASE}/account/generate-api-key",
                            headers={"Authorization": f"Bearer {st.session_state.token}"}
                        )
                        if r.status_code == 200:
                            # Actually we can just rely on the user re-fetching on next run or forcing a sign-in refresh
                            st.success("API Key generated! Please refresh the page.")
                        else:
                            st.error("Failed to generate API Key.")
                else:
                    st.warning("API Access is only available on the Pro and Advanced tiers.")
"""

content = re.sub(pattern, r'\1' + new_ui, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Regex injected into Profile.")
