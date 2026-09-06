import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update the price
content = content.replace('14,999', '99,999')
content = content.replace('14999', '99999')

# Now inject the dialog component and modify the profile section
old_ui = """                if user.get("tier") == "advanced":
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

new_ui = """                if user.get("tier") == "advanced":
                    current_key_exists = bool(user.get("api_key"))
                    
                    if current_key_exists:
                        st.success("✅ Your Enterprise API Key is active (Hidden for security).")
                        st.caption("Pass your **API Secret** in the `X-API-Key` HTTP header to authenticate.")
                    else:
                        st.info("You haven't generated an API Key yet.")
                    
                    # We define a function for the modal popup
                    @st.dialog("🔑 Generate API Key", width="large")
                    def show_api_key_modal():
                        st.warning("⚠️ CRITICAL: Copy your API Secret now. For security reasons, it will NEVER be shown again once you close this window!")
                        import requests
                        with st.spinner("Provisioning enterprise credentials..."):
                            r = requests.post(
                                f"{API_BASE}/account/generate-api-key",
                                headers={"Authorization": f"Bearer {st.session_state.token}"}
                            )
                        if r.status_code == 200:
                            data = r.json()
                            st.text_input("API Key ID (Public)", value=data.get("api_key_id", ""), disabled=True)
                            
                            st.markdown("### API Secret")
                            st.code(data.get("api_secret", ""), language="text")
                            
                            st.info("Please store this securely in your environment variables or secret manager (e.g., AWS Secrets Manager, GCP Secret Manager).")
                            if st.button("I have copied my API Secret"):
                                # Refresh user state to show the success badge
                                me_res = api_get("/auth/me")
                                if me_res["ok"]: st.session_state.user = me_res["data"]
                                st.rerun()
                        else:
                            st.error("Failed to generate API Key.")
                            
                    if st.button("Generate New API Key", type="primary"):
                        show_api_key_modal()"""

content = content.replace(old_ui, new_ui)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated frontend UI for Modal API Keys and Price.")
