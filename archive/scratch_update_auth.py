import sys

file_path = 'app/auth.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '"pro":      {"compare_max": 5,  "api_daily": 1000,  "export": True,  "find_similar": True},',
    '"pro":      {"compare_max": 5,  "api_daily": 0,     "export": True,  "find_similar": True},'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated auth.py")
