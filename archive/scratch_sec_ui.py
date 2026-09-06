import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the API Key UI logic
old_ui = """                if user.get("tier") == "advanced":
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
                            st.error("Failed to generate API Key.")"""

new_ui = """                if user.get("tier") == "advanced":
                    current_key_exists = bool(user.get("api_key"))
                    
                    if current_key_exists:
                        st.success("✅ Your Enterprise API Key is active (Hidden for security).")
                        st.caption("Pass your API key in the `X-API-Key` HTTP header to authenticate.")
                    else:
                        st.info("You haven't generated an API Key yet.")
                        
                    if st.session_state.get("new_api_key"):
                        st.warning("⚠️ CRITICAL: Copy your API Key now. It will NEVER be shown again!")
                        st.code(st.session_state["new_api_key"], language="text")
                    
                    if st.button("Generate New API Key"):
                        import requests
                        r = requests.post(
                            f"{API_BASE}/account/generate-api-key",
                            headers={"Authorization": f"Bearer {st.session_state.token}"}
                        )
                        if r.status_code == 200:
                            st.session_state["new_api_key"] = r.json()["api_key"]
                            # Refresh user state to show the success badge
                            me_res = api_get("/auth/me")
                            if me_res["ok"]: st.session_state.user = me_res["data"]
                            st.rerun()
                        else:
                            st.error("Failed to generate API Key.")"""

content = content.replace(old_ui, new_ui)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated frontend UI for Show-Once API Keys.")
