import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We will inject the API Key UI into the Subscriptions section or the main Account dashboard
target_code = """
          st.markdown("### 💎 Subscriptions & Upgrades")"""

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
          
          st.markdown("### 💎 Subscriptions & Upgrades")"""

if target_code in content:
    content = content.replace(target_code, new_ui, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added API Key UI to frontend.")
else:
    print("Could not find Subscriptions section.")
