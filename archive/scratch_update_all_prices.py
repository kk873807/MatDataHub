import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the sidebar buttons
content = re.sub(r'Request Upgrade to Pro — ₹.*?/mo', 'Request Upgrade to Pro — ₹499/mo', content)
content = re.sub(r'Request Upgrade to Advanced — ₹.*?/mo', 'Request Upgrade to Advanced — ₹49,999/mo', content)

# Fix the pricing page for Pro
content = re.sub(r'st\.markdown\("## ₹1499 / mo"\)', 'st.markdown("## ₹499 / mo")', content)

# Fix AI Advisor Upsell button
content = re.sub(r'Upgrade to Pro \(Rs\. 1499/mo\)', 'Upgrade to Pro (Rs. 499/mo)', content)

# Also fix the weird encoding symbols if they exist in the raw file (powershell just outputs them weirdly but let's be safe)
# The symbol ₹ is fine if the file is utf-8. We can just use the literal text.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated frontend prices via regex")
