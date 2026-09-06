import sys

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_smtp = """        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)"""

new_smtp = """        # Strip spaces from App Password (users often copy it with spaces)
        sender_password = sender_password.replace(" ", "")
        
        # Use SMTP_SSL on port 465 to bypass firewall/port blocks
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)"""

if old_smtp in content:
    content = content.replace(old_smtp, new_smtp)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("feedback.py SMTP logic updated to 465 SSL.")
else:
    print("Could not find old SMTP in feedback.py.")
