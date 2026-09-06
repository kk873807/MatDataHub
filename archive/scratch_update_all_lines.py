import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "Request Upgrade to Pro" in line:
        line = '            if st.button("🚀 Request Upgrade to Pro — ₹499/mo"):\n'
    if "Request Upgrade to Advanced" in line:
        line = '            if st.button("💎 Request Upgrade to Advanced — ₹49,999/mo"):\n'
    if 'st.markdown("## ₹1499 / mo")' in line:
        line = '            st.markdown("## ₹499 / mo")\n'
    if 'Upgrade to Pro (Rs. 1499/mo)' in line:
        line = line.replace('1499', '499')
    new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Updated all frontend lines.")
