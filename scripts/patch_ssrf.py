import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\materials.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for SSRF protection
if 'import urllib.parse' not in content:
    content = content.replace('import requests\n', 'import requests\nimport urllib.parse\nimport socket\nimport ipaddress\n')

# Define the helper
ssrf_helper = '''
def is_safe_url(url: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ['http', 'https']: return False
        if not parsed.hostname: return False
        ip = socket.gethostbyname(parsed.hostname)
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local: return False
        return True
    except Exception:
        return False
'''

if 'def is_safe_url' not in content:
    # insert before create_custom_material
    idx = content.find('@router.post("/custom",')
    content = content[:idx] + ssrf_helper + '\n' + content[idx:]

# Update the validation logic
old_val = '''    if not getattr(mat, 'source_url', None) or not str(mat.source_url).startswith('http'):
        raise HTTPException(status_code=400, detail="A valid source_url (http/https) is required.")
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(mat.source_url, headers=headers, timeout=10, allow_redirects=True, stream=True)
        r.close()'''

new_val = '''    if not getattr(mat, 'source_url', None) or not str(mat.source_url).startswith('http'):
        raise HTTPException(status_code=400, detail="A valid source_url (http/https) is required.")
        
    if not is_safe_url(str(mat.source_url)):
        raise HTTPException(status_code=400, detail="Invalid or unsafe Source URL (SSRF blocked).")
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(str(mat.source_url), headers=headers, timeout=10, allow_redirects=True, stream=True)
        r.close()'''

if old_val in content:
    content = content.replace(old_val, new_val)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SSRF protection added!")
else:
    print("Could not find validation logic to patch.")
