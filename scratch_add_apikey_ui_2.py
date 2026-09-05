import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_ui = """
        # --- API KEY SECTION ---
        if curr_user.get("tier") in ["pro", "advanced"]:
            st.markdown("### 🔑 API Access")
            current_key = curr_user.get("api_key")
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
                    st.success("API Key generated!")
                    st.rerun()
                else:
                    st.error("Failed to generate API Key.")
"""

# We'll inject it right before: st.markdown("### 💎 Subscriptions & Upgrades")
content = re.sub(
    r'(st\.markdown\("### .*?Subscriptions & Upgrades"\))',
    new_ui + r'\n        \1',
    content
)

# And fix the text "API Access is currently restricted to Enterprise"
content = content.replace(
    'API Access is currently restricted to Enterprise customers to prevent data scraping. If you require programmatic access for a commercial application, please contact support for an Enterprise contract.',
    'API Access is available on the Pro and Advanced tiers! You can generate your secure `X-API-Key` directly from this Account Dashboard once you upgrade.'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated frontend UI for API Keys.")
