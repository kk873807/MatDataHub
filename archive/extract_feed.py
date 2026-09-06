import sys

with open("old_app.py", "r", encoding="utf-8") as f:
    content = f.read()
    
start = content.find('st.markdown("## Community Reviews & Discussion")')
end = content.find('    with tab_browse:', start)

text = content[start:end]
print(text.encode("ascii", "ignore").decode())
