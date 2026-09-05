import sys

file_path = 'app/routers/admin.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the SSL logic with forced IPv4
old_ssl = """        # Use SMTP_SSL on port 465 (often bypasses Render/ISP port 587 blocks)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)"""

new_ssl = """        import socket
        # Force IPv4 resolution to prevent [Errno 101] IPv6 routing bugs in containers
        ipv4_address = socket.gethostbyname('smtp.gmail.com')
        
        # Use SMTP_SSL on port 465 (often bypasses Render/ISP port 587 blocks)
        server = smtplib.SMTP_SSL(ipv4_address, 465)
        # We need to tell the server we are connecting to smtp.gmail.com for SSL certificate validation
        server.ehlo('smtp.gmail.com')"""

if old_ssl in content:
    content = content.replace(old_ssl, new_ssl)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("admin.py IPv4 fallback added.")
else:
    print("Could not find old SSL in admin.py.")
