import re

with open('next-frontend/src/app/analytics/cbam/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('7318 15 00', '7318 15 20')

with open('next-frontend/src/app/analytics/cbam/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated demo code")
