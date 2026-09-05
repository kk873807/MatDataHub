import sys

with open("old_app.py", "r", encoding="utf-16") as f:
    content = f.read()

start = content.find('st.markdown("## Community Reviews & Discussion")')
end = content.find('    #  TAB: BROWSE MATERIALS', start)

if start != -1:
    text = content[start-40:end]
    print(text.encode("ascii", "ignore").decode())
else:
    print("NOT FOUND IN old_app.py")
