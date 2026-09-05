import sys
import re

# Update Payments
file_path_pay = 'app/routers/payments.py'
with open(file_path_pay, 'r', encoding='utf-8') as f:
    content_pay = f.read()

content_pay = content_pay.replace('9999900', '4999900')

with open(file_path_pay, 'w', encoding='utf-8') as f:
    f.write(content_pay)

# Update UI
file_path_ui = 'frontend/app.py'
with open(file_path_ui, 'r', encoding='utf-8') as f:
    content_ui = f.read()

content_ui = content_ui.replace('99,999', '49,999')
content_ui = content_ui.replace('99999', '49999')

with open(file_path_ui, 'w', encoding='utf-8') as f:
    f.write(content_ui)

print("Updated pricing to 49,999 INR.")
