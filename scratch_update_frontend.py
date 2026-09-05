import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the SMTP debugger UI
smtp_debugger_pattern = r'# --- NEW SMTP DEBUGGER ---.*?st\.info\("HINT: If you are using Gmail.*?"\)'
content = re.sub(smtp_debugger_pattern, '', content, flags=re.DOTALL)

# Update the button text
content = content.replace('if st.form_submit_button("Send Official Reply & Email"):', 'if st.form_submit_button("Post Official Admin Reply"):')
content = content.replace('st.caption("This will email the user and lock an official admin response to this thread.")', 'st.caption("This will lock a verified official admin response to this thread.")')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Frontend updated: Removed SMTP debugger and updated reply button.")
