with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

bad_sub = """        user = st.session_state.get("user")
        token = st.session_state.get("token")
        if not token or not user:
            st.warning("You must be logged in to use this feature.")
        else:
            user_tier = user.get("tier", "free")
        if user_tier == "free":
            st.info(" The Smart Substitution Engine is available on **Pro** and **Advanced** tiers. Upgrade to unlock interactive multi-objective optimization.")
        else:"""

good_sub = """        token = st.session_state.get("token")
        user = st.session_state.get("user", {})
        
        if not token:
            st.warning("You must be logged in to use this feature.")
        elif user.get("tier", "free") == "free":
            st.info(" The Smart Substitution Engine is available on **Pro** and **Advanced** tiers. Upgrade to unlock interactive multi-objective optimization.")
        else:"""

content = content.replace(bad_sub, good_sub)

bad_ent = """        user = st.session_state.get("user")
        user_tier = user.get("tier", "free") if user else "free"
        
        if not user or not st.session_state.get("token"):
            st.warning("You must be logged in to use this feature.")
        elif user_tier != "advanced":"""

good_ent = """        token = st.session_state.get("token")
        user = st.session_state.get("user", {})
        user_tier = user.get("tier", "free") if isinstance(user, dict) else "free"
        
        if not token:
            st.warning("You must be logged in to use this feature.")
        elif user_tier != "advanced":"""

content = content.replace(bad_ent, good_ent)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Auth logic fixed again!")
