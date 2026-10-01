import re
path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_jsx = '            <MaterialManager secret={secret} />'

new_jsx = '''            <MaterialManager secret={secret} />
            
            {/* User Contributions */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-950/50">
                <div className="flex items-center gap-3">
                  <Database className="w-5 h-5 text-cyan-500" />
                  <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">User Material Contributions</h2>
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-950/80 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider">
                    <tr>
                      <th className="px-6 py-4 font-semibold">User</th>
                      <th className="px-6 py-4 font-semibold text-center">Total Added</th>
                      <th className="px-6 py-4 font-semibold">Materials (Latest 5)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {contributions.map((c: any) => (
                      <tr key={c.user.id} className="hover:bg-slate-100 dark:hover:bg-slate-800/30 transition-colors">
                        <td className="px-6 py-4">
                          <div className="font-bold text-slate-900 dark:text-white">{c.user.name}</div>
                          <div className="text-slate-500 dark:text-slate-400 text-xs">{c.user.email}</div>
                          <div className="mt-1 text-[10px] uppercase font-bold text-slate-500 bg-slate-200 dark:bg-slate-800 inline-block px-1 rounded">{c.user.tier}</div>
                        </td>
                        <td className="px-6 py-4 text-center">
                          <span className="text-lg font-bold text-cyan-600 dark:text-cyan-400 bg-cyan-100 dark:bg-cyan-900/30 px-3 py-1 rounded-full">
                            {c.materials.length}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex flex-wrap gap-2">
                            {c.materials.slice(0, 5).map((m: any) => (
                              <div key={m.id} className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs">
                                <span className="font-semibold block line-clamp-1">{m.name}</span>
                                <span className="text-slate-500 text-[10px]">{m.category}</span>
                              </div>
                            ))}
                            {c.materials.length > 5 && (
                              <div className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs flex items-center justify-center font-bold text-slate-500">
                                +{c.materials.length - 5} more
                              </div>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                    {contributions.length === 0 && (
                      <tr><td colSpan={3} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400">No custom materials contributed yet.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>'''

if old_jsx in content:
    content = content.replace(old_jsx, new_jsx)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("JSX updated")
else:
    print("JSX marker not found")

# We need Database icon from lucide-react if not imported
if 'Database' not in content[:content.find(';')]:
    content = content.replace('import { ShieldAlert, Check, X, Lock, Users, MessageSquare, FileText, Plus }', 'import { ShieldAlert, Check, X, Lock, Users, MessageSquare, FileText, Plus, Database }')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
