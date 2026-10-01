import re
path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add state
if 'const [contributions' not in content:
    content = content.replace(
        'const [feedback, setFeedback] = useState<any[]>([]);',
        'const [feedback, setFeedback] = useState<any[]>([]);\n  const [contributions, setContributions] = useState<any[]>([]);'
    )

# Update fetchAdminData
old_fetch = '''      const [reqRes, feedRes] = await Promise.all([
        fetch(`${API}/admin/upgrade-requests`, {
          headers: { "X-Admin-Secret": adminSecret }
        }),
        fetch(`${API}/feedback/`, {
          headers: { "X-Admin-Secret": adminSecret }
        })
      ]);'''
new_fetch = '''      const [reqRes, feedRes, contribRes] = await Promise.all([
        fetch(`${API}/admin/upgrade-requests`, {
          headers: { "X-Admin-Secret": adminSecret }
        }),
        fetch(`${API}/feedback/`, {
          headers: { "X-Admin-Secret": adminSecret }
        }),
        fetch(`${API}/admin/user-contributions`, {
          headers: { "X-Admin-Secret": adminSecret }
        })
      ]);'''
content = content.replace(old_fetch, new_fetch)

old_feedres_ok = '''      if (feedRes.ok) {
        setFeedback(await feedRes.json());
      }'''
new_feedres_ok = '''      if (feedRes.ok) {
        setFeedback(await feedRes.json());
      }
      if (contribRes.ok) {
        setContributions(await contribRes.json());
      }'''
content = content.replace(old_feedres_ok, new_feedres_ok)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("State and fetch updated")
