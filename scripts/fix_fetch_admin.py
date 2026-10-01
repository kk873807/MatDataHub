import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('fetchAdminData(secret)', 'fetchAdminData(localStorage.getItem("token") || "")')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed fetchAdminData refresh calls")
