import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\account\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''    if (!token) {
      setError("Not logged in");
      setLoading(false);
      return;
    }'''

good = '''    if (!token) {
      // Force redirect to login if no token is found, preventing infinite "Authenticating..." spinner
      window.location.href = "/?login=true";
      return;
    }'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed infinite Authenticating spinner on Account page")
else:
    print("Could not find block")
