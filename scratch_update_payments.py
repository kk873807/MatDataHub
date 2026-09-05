import sys

file_path = 'app/routers/payments.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Currently it probably says: amount = 49900 if tier == "pro" else 149900
content = content.replace(
    'amount = 49900 if tier == "pro" else 149900',
    'amount = 49900 if tier == "pro" else 1499900'  # 14,999 INR
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated payments.py")
