import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# First, update the st.tabs declaration for Support Center
old_support_tabs = '        tab_feedback, = st.tabs(["🎫 Submit Support Ticket"])'
new_support_tabs = '        tab_community, tab_feedback = st.tabs(["💬 Community Discussions", "🎫 Submit Support Ticket"])'
content = content.replace(old_support_tabs, new_support_tabs)

# Now, we read the community_feed_extracted.py
with open("community_feed_extracted.py", "r", encoding="utf-8") as f:
    feed_code = f.read()

# Clean up the mangled text
feed_code = feed_code.replace("I\"AA%", "⭐")
feed_code = feed_code.replace("html=True)\n        st.divider()\n", "")

# We need to wrap it inside `with tab_community:`
# Let's indent it by replacing \n        with \n            
indented_feed = feed_code.replace("\n        ", "\n            ")
indented_feed = "    with tab_community:\n            " + indented_feed

# We'll inject it right before `with tab_feedback:`
old_tab_feedback = "    with tab_feedback:"
new_tab_feedback = indented_feed + "\n\n" + old_tab_feedback

content = content.replace(old_tab_feedback, new_tab_feedback)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Injected Community feed to Support Center!")
