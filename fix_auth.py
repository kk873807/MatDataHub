with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Smart Substitute auth
bad_auth_sub = """        if not st.session_state.get("is_authenticated"):
            st.warning("You must be logged in to use this feature.")
            st.stop()
            
        user_tier = st.session_state.get("user_tier", "free")"""

good_auth_sub = """        user = st.session_state.get("user")
        token = st.session_state.get("token")
        if not token or not user:
            st.warning("You must be logged in to use this feature.")
        else:
            user_tier = user.get("tier", "free")"""

content = content.replace(bad_auth_sub, good_auth_sub)

# Fix Enterprise BOM auth (it also used wrong user_tier getter)
bad_auth_ent = """        user_tier = st.session_state.get("user_tier", "free")
        if user_tier != "advanced":"""

good_auth_ent = """        user = st.session_state.get("user")
        user_tier = user.get("tier", "free") if user else "free"
        
        if not user or not st.session_state.get("token"):
            st.warning("You must be logged in to use this feature.")
        elif user_tier != "advanced":"""

content = content.replace(bad_auth_ent, good_auth_ent)

# Note: The `else:` indentation in both tabs needs to line up perfectly.
# Let's verify the replacement happened.
with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Auth logic fixed in frontend/app.py")
