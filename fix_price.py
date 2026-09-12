import os

filepath = 'app/routers/payments.py'
with open(filepath, 'r') as f:
    content = f.read()

# Replace 4999900 with 1999900
content = content.replace('4999900', '1999900')

with open(filepath, 'w') as f:
    f.write(content)

print("Updated advanced tier price in backend to 19999")
