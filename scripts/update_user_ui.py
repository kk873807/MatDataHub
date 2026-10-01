import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AdvancedMaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_ui = '''                  {myMaterials.map((m, i) => (
                    <li key={i} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-3 shadow-sm hover:shadow-md transition-shadow">
                      <p className="font-semibold text-sm text-slate-900 dark:text-white line-clamp-1">{m.name}</p>
                      <div className="flex justify-between items-center mt-1">
                        <span className="text-xs font-medium text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded">{m.category}</span>
                        <span className="text-[10px] text-slate-400 dark:text-slate-500">{m.created_at ? new Date(m.created_at).toLocaleDateString() : ''}</span>
                      </div>
                    </li>
                  ))}'''

new_ui = '''                  {myMaterials.map((m: any, i) => (
                    <li key={m.id || i} className={`bg-white dark:bg-slate-900 border rounded-lg p-3 shadow-sm hover:shadow-md transition-shadow ${m.status === 'approved' ? 'border-emerald-200 dark:border-emerald-800/50' : m.status === 'rejected' ? 'border-red-200 dark:border-red-800/50' : 'border-slate-200 dark:border-slate-800'}`}>
                      <div className="flex justify-between items-start">
                        <p className="font-semibold text-sm text-slate-900 dark:text-white line-clamp-1">{m.name}</p>
                        <span className={`text-[9px] uppercase font-bold px-1.5 py-0.5 rounded ${m.status === 'approved' ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400' : m.status === 'rejected' ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400' : 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400'}`}>
                          {m.status || 'pending'}
                        </span>
                      </div>
                      <div className="flex justify-between items-center mt-2">
                        <span className="text-xs font-medium text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded">{m.category}</span>
                        <span className="text-[10px] text-slate-400 dark:text-slate-500">{m.created_at ? new Date(m.created_at).toLocaleDateString() : ''}</span>
                      </div>
                    </li>
                  ))}'''

if old_ui in content:
    content = content.replace(old_ui, new_ui)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated AdvancedMaterialManager UI")
else:
    print("UI block not found")
