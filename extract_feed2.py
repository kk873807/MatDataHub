import sys

with open("old_app.py", "r", encoding="utf-16") as f:
    content = f.read()
    
start = content.find('st.markdown("## Community Reviews & Discussion")')
end = content.find('    with tab_browse:', start)

if start == -1:
    print("Not found")
else:
    text = content[start-20:end]
    print(text.encode("ascii", "ignore").decode())
