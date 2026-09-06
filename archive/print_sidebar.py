import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()
    
# Let's extract the sidebar portion
sidebar_idx = content.find("with st.sidebar:")
if sidebar_idx != -1:
    end_idx = content.find("if st.session_state.current_page ==", sidebar_idx)
    text = content[sidebar_idx:end_idx]
    text = text.encode("ascii", "ignore").decode()
    print(text)
else:
    print("Sidebar not found")
