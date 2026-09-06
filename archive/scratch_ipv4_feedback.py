import sys

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """        # Strip spaces from App Password (users often copy it with spaces)
        sender_password = sender_password.replace(" ", "")
        
        # Use SMTP_SSL on port 465 to bypass firewall/port blocks
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()"""

new_logic = """        # Strip spaces from App Password (users often copy it with spaces)
        sender_password = sender_password.replace(" ", "")
        
        import socket
        orig_getaddrinfo = socket.getaddrinfo
        def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
            return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
        socket.getaddrinfo = getaddrinfo_ipv4
        
        try:
            # Use SMTP_SSL on port 465 to bypass firewall/port blocks
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
        finally:
            socket.getaddrinfo = orig_getaddrinfo"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("feedback.py IPv4 monkey-patch added.")
else:
    print("Could not find old logic in feedback.py.")
