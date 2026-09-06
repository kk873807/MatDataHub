import sys

file_path = 'app/routers/admin.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert back to using hostname
old_bad = """        import socket
        # Force IPv4 resolution to prevent [Errno 101] IPv6 routing bugs in containers
        ipv4_address = socket.gethostbyname('smtp.gmail.com')
        
        # Use SMTP_SSL on port 465 (often bypasses Render/ISP port 587 blocks)
        server = smtplib.SMTP_SSL(ipv4_address, 465)
        # We need to tell the server we are connecting to smtp.gmail.com for SSL certificate validation
        server.ehlo('smtp.gmail.com')"""

new_good = """        import socket
        # Monkey-patch getaddrinfo to force IPv4 (AF_INET) to prevent IPv6 [Errno 101] Unreachable errors in Render
        orig_getaddrinfo = socket.getaddrinfo
        def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
            return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
        socket.getaddrinfo = getaddrinfo_ipv4
        
        try:
            # Use SMTP_SSL on port 465 (often bypasses Render/ISP port 587 blocks)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_password)
        finally:
            # Restore original getaddrinfo
            socket.getaddrinfo = orig_getaddrinfo"""

if old_bad in content:
    content = content.replace(old_bad, new_good)
    
    # Let's fix the login logic to correctly capture it
    # Oh wait, server.quit() is below this.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("admin.py IPv4 monkey-patch added.")
else:
    print("Could not find old bad in admin.py.")
