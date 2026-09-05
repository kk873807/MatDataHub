import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix the mangled text
content = content.replace("\u2261\u0192\xe6\xec Helpful", "👍 Helpful")
content = content.replace("\u2261\u0192\xc6\xbc Reply", "💬 Reply")
content = content.replace("\u2261\u0192\xa2\xe1\u2229\u2555\xc5 Admin", "🛡️ Admin")
content = content.replace("I\"AA%", "⭐")

# 2. Extract tab_community
start_marker = "    with tab_community:"
end_marker = "    with tab_feedback:"
start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    community_block = content[start_idx:end_idx]
    # Remove the `with tab_community:` part and adjust indentation
    # Currently it's indented like:
    #     with tab_community:
    #         st.markdown(...)
    # We want to put it in `tab_home`, which means it should just be:
    #         st.markdown(...)
    
    lines = community_block.split("\n")
    # Remove the first line (`with tab_community:`)
    lines = lines[1:]
    
    # We don't need to unindent, `tab_home` contents are also indented 8 spaces!
    cleaned_community_block = "\n".join(lines)
    
    # Remove it from its current location
    content = content[:start_idx] + content[end_idx:]
    
    # 3. Append to tab_home
    # Find the end of tab_home. tab_home ends right before `with tab_browse_main:` or `with tab_guide:`?
    # No, wait, currently tab_home ends where? Let's find the end of tab_home block.
    # Actually, tab_home ends where tab_browse_main begins.
    home_end_marker = "    with tab_browse_main:"
    home_end_idx = content.find(home_end_marker)
    
    if home_end_idx != -1:
        # We append the community block to the end of tab_home
        content = content[:home_end_idx] + "\n        st.markdown('---')\n" + cleaned_community_block + "\n" + content[home_end_idx:]
    
    # 4. Update the st.tabs definition in Support Center to remove tab_community
    old_support_tabs = '        tab_community, tab_feedback = st.tabs(["💬 Community Discussions", "🎫 Submit Support Ticket"])'
    new_support_tabs = '        tab_feedback, = st.tabs(["🎫 Submit Support Ticket"])'
    content = content.replace(old_support_tabs, new_support_tabs)
    
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Community block moved and emojis fixed!")
else:
    print("Could not find community block")
