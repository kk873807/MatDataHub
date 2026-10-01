import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_handler = '''  const handleMaterialAction = async (contribId: number, action: "approve" | "reject") => {
    try {
      const res = await fetch(`${API}/admin/contributions/${contribId}/${action}`, {
        method: "POST",
        headers: { "X-Admin-Secret": secret }
      });
      if (res.ok) {
        fetchAdminData(secret);
      } else {
        const err = await res.json();
        alert(err.detail || "Failed to perform action");
      }
    } catch (err) {
      alert("Network error.");
    }
  };'''

if 'handleMaterialAction' not in content:
    content = content.replace(
        'const handleAction = async (userId: number, action: "approve" | "reject") => {',
        new_handler + '\n\n  const handleAction = async (userId: number, action: "approve" | "reject") => {'
    )
    
old_map = '''                            {c.materials.slice(0, 5).map((m: any) => (
                              <div key={m.id} className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs">
                                <span className="font-semibold block line-clamp-1">{m.name}</span>
                                <span className="text-slate-500 text-[10px]">{m.category}</span>
                              </div>
                            ))}'''

new_map = '''                            {c.materials.slice(0, 5).map((m: any) => (
                              <div key={m.id} className={`border rounded-lg p-2 text-xs flex flex-col ${m.status === 'approved' ? 'bg-emerald-50 dark:bg-emerald-900/30 border-emerald-200 dark:border-emerald-800' : m.status === 'rejected' ? 'bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800' : 'bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700'}`}>
                                <div>
                                  <span className="font-semibold block line-clamp-1 dark:text-white">{m.name}</span>
                                  <span className="text-slate-500 dark:text-slate-400 text-[10px]">{m.category}</span>
                                </div>
                                {m.status === 'pending' && (
                                  <div className="flex gap-1 mt-2">
                                    <button onClick={() => handleMaterialAction(m.id, 'approve')} className="bg-emerald-500 hover:bg-emerald-600 text-white rounded px-2 py-0.5 text-[10px] transition-colors">Approve</button>
                                    <button onClick={() => handleMaterialAction(m.id, 'reject')} className="bg-red-500 hover:bg-red-600 text-white rounded px-2 py-0.5 text-[10px] transition-colors">Reject</button>
                                  </div>
                                )}
                                {m.status !== 'pending' && (
                                  <span className={`text-[9px] uppercase font-bold mt-1 ${m.status === 'approved' ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>{m.status}</span>
                                )}
                              </div>
                            ))}'''

content = content.replace(old_map, new_map)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated admin/page.tsx with handlers and UI")
