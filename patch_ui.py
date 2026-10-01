import os

file_path = 'next-frontend/src/app/materials/[id]/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
for i, line in enumerate(lines):
    if 'const [isPriceLocked, setIsPriceLocked] = useState(false);' in line:
        out.append(line)
        out.append('  const [isSaved, setIsSaved] = useState(false);\n')
        out.append('  const [saving, setSaving] = useState(false);\n')
        continue
    
    if '// Fetch Similar' in line:
        out.append('        // Fetch Saved Status\n')
        out.append('        const savedRes = await fetch(`${API}/materials/me/saved`, { headers });\n')
        out.append('        if (savedRes.ok) {\n')
        out.append('          const savedList = await savedRes.json();\n')
        out.append('          setIsSaved(savedList.some((m: any) => m.id === parseInt(id as string)));\n')
        out.append('        }\n\n')
        out.append(line)
        continue
        
    if 'const showToast = (msg: string) => {' in line:
        out.append('''  const toggleSave = async () => {
    const token = localStorage.getItem("token");
    if (!token) return showToast("Log in to save materials");
    setSaving(true);
    try {
      const res = await fetch(`${API}/materials/${id}/save`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setIsSaved(data.status === 'saved');
        showToast(data.status === 'saved' ? "Material Saved!" : "Material Unsaved");
      }
    } catch (e) {
      console.error(e);
    }
    setSaving(false);
  };
''')
        out.append(line)
        continue
        
    if 'import {' in line and 'Sparkles' in lines[i+1] if i+1 < len(lines) else False:
        out.append(line)
        continue
        
    if 'Sparkles' in line and 'lucide-react' not in line:
        out.append(line.replace('Sparkles', 'Sparkles, Bookmark'))
        continue

    if 'Add to Compare' in line:
        out.append(line)
        out.append('                </Link>\n')
        out.append('''                <button
                  onClick={toggleSave}
                  disabled={saving}
                  className={`flex items-center gap-2 px-4 py-2 rounded-2xl text-sm font-bold transition-all shadow-lg ${isSaved ? 'bg-emerald-600 text-white shadow-emerald-900/20 hover:bg-emerald-700' : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700'}`}
                >
                  <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-current' : ''}`} /> {isSaved ? 'Saved' : 'Save'}
                </button>\n''')
        continue
        
    if '</Link>' in line and 'Add to Compare' in lines[i-1]:
        # skip this because I appended it manually above
        continue
        
    out.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(out)
