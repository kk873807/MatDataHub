with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('"🔍 Database"', '"🔍 Browse Materials"')
# Also check if it's written as 'Database' in other prominent places where it means the tab
# For example, if there's a st.header("Database") or similar inside the tab
content = content.replace('st.header("Database")', 'st.header("Browse Materials")')
content = content.replace('st.title("Material Database")', 'st.title("Browse Materials")')

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Tab renamed successfully.")
