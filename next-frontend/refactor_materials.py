# -*- coding: utf-8 -*-
import os
import re

filepath = r'src\app\materials\page.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Add LayoutGrid and List to lucide-react imports
if 'LayoutGrid' not in text:
    text = text.replace('import { Search', 'import { LayoutGrid, List, Search')

# Add viewMode state
if 'const [viewMode' not in text:
    text = text.replace(
        'const [sortBy, setSortBy] = useState("name_asc");',
        'const [sortBy, setSortBy] = useState("name_asc");\n  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");'
    )

# Replace the Filters button container to include the View Toggle
view_toggle_html = '''
              <div className="flex bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-1">
                <button 
                  onClick={() => setViewMode('grid')}
                  className={p-2 rounded-lg transition-all }
                >
                  <LayoutGrid className="w-5 h-5" />
                </button>
                <button 
                  onClick={() => setViewMode('table')}
                  className={p-2 rounded-lg transition-all }
                >
                  <List className="w-5 h-5" />
                </button>
              </div>

              <button 
'''
text = text.replace('<button \n                onClick={() => setShowFilters(!showFilters)}', view_toggle_html.strip() + ' \n                onClick={() => setShowFilters(!showFilters)}')


# Update the Render to conditionally show grid or table
grid_start = '<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">'

table_view_html = '''
          {viewMode === 'table' ? (
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-sm">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm whitespace-nowrap">
                  <thead>
                    <tr className="bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800">
                      <th className="px-6 py-4 font-semibold text-slate-900 dark:text-white uppercase tracking-wider text-xs">Material Name</th>
                      <th className="px-6 py-4 font-semibold text-slate-900 dark:text-white uppercase tracking-wider text-xs">Category</th>
                      <th className="px-6 py-4 font-semibold text-slate-900 dark:text-white uppercase tracking-wider text-xs">Yield Strength</th>
                      <th className="px-6 py-4 font-semibold text-slate-900 dark:text-white uppercase tracking-wider text-xs">Density</th>
                      <th className="px-6 py-4 font-semibold text-slate-900 dark:text-white uppercase tracking-wider text-xs">Est. Cost</th>
                      <th className="px-6 py-4 font-semibold text-slate-900 dark:text-white uppercase tracking-wider text-xs text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-slate-800/50">
                    {sortedMaterials.map((mat, i) => (
                      <tr key={mat.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors group">
                        <td className="px-6 py-4">
                          <Link href={/materials/} className="font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors text-base">
                            {mat.name}
                          </Link>
                        </td>
                        <td className="px-6 py-4">
                          <span className={inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold }>
                            {mat.category}
                          </span>
                        </td>
                        <td className="px-6 py-4 font-medium text-slate-700 dark:text-slate-300">
                          {mat.yield_strength_min || '-'} <span className="text-slate-400 font-normal text-xs">MPa</span>
                        </td>
                        <td className="px-6 py-4 font-medium text-slate-700 dark:text-slate-300">
                          {mat.density || '-'} <span className="text-slate-400 font-normal text-xs">g/cm3</span>
                        </td>
                        <td className="px-6 py-4 font-bold text-emerald-600 dark:text-emerald-400">
                          ₹{mat.cost_per_kg_min || '-'} <span className="text-slate-400 font-normal text-xs">/kg</span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <Link href={/materials/} className="inline-flex items-center justify-center px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-emerald-500 hover:text-emerald-600 dark:hover:text-emerald-400 text-slate-700 dark:text-slate-300 rounded-lg text-xs font-bold transition-all shadow-sm">
                            View Details
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
'''

if 'viewMode ===' not in text:
    text = text.replace(grid_start, table_view_html + grid_start)
    text = text.replace('          </div>\n        )}\n\n        {/* Free tier upgrade banner */}', '          </div>\n          )}\n        )}\n\n        {/* Free tier upgrade banner */}')

# Enhance Grid Cards with visual Data Bars
data_bars_html = '''
                    <div className="space-y-3.5 text-sm mt-auto relative z-10 bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200/60 dark:border-slate-800/60">
                      <div>
                        <div className="flex justify-between items-center mb-1.5">
                          <span className="text-slate-500 dark:text-slate-400 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider"><TrendingUp className="w-3.5 h-3.5" /> Yield</span>
                          <span className="text-slate-900 dark:text-white font-bold">{mat.yield_strength_min || '-'} <span className="text-slate-500 dark:text-slate-400 text-xs font-normal">MPa</span></span>
                        </div>
                        <div className="w-full bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">
                          <div className="bg-emerald-500 h-full rounded-full" style={{ width: ${Math.min(((mat.yield_strength_min || 0) / 1000) * 100, 100)}% }}></div>
                        </div>
                      </div>
                      
                      <div>
                        <div className="flex justify-between items-center mb-1.5">
                          <span className="text-slate-500 dark:text-slate-400 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider"><Scale className="w-3.5 h-3.5" /> Density</span>
                          <span className="text-slate-900 dark:text-white font-bold">{mat.density || '-'} <span className="text-slate-500 dark:text-slate-400 text-xs font-normal">g/cm3</span></span>
                        </div>
                        <div className="w-full bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">
                          <div className="bg-blue-500 h-full rounded-full" style={{ width: ${Math.min(((mat.density || 0) / 20) * 100, 100)}% }}></div>
                        </div>
                      </div>

                      <div className="flex justify-between items-center pt-3 mt-3 border-t border-slate-200 dark:border-slate-800">
                        <span className="text-slate-500 dark:text-slate-400 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider"><Zap className="w-3.5 h-3.5" /> Est. Cost</span>
                        <span className="text-emerald-600 dark:text-emerald-400 font-black text-base">₹{mat.cost_per_kg_min || '-'}<span className="text-xs font-medium text-emerald-600/70 dark:text-emerald-400/70">/kg</span></span>
                      </div>
                    </div>
'''
text = re.sub(r'<div className="space-y-2\.5 text-sm mt-auto relative z-10">.*?</div>\s*</Link>', data_bars_html.strip() + '\n                  </Link>', text, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)