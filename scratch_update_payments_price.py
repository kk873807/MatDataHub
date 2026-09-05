import sys

file_path = 'app/routers/payments.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('1499900', '9999900')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated payments.py price to 99999 INR")
