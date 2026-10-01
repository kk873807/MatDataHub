import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "r", encoding="utf-8") as f:
    code = f.read()

old_excluded_label = """{((totalCO2/1000) - taxableTonnes).toLocaleString(undefined, { maximumFractionDigits: 1 })} t excluded (exempt origin/dest or carbon price paid)"""
new_excluded_label = """{((totalCO2/1000) - taxableTonnes).toLocaleString(undefined, { maximumFractionDigits: 1 })} t-equivalent excluded (exempt origin/dest or carbon price paid)"""
code = code.replace(old_excluded_label, new_excluded_label)

old_dropdown_title = """<p className="text-slate-500 dark:text-slate-400 font-medium flex items-center gap-2"><FileText className="w-4 h-4 text-amber-600 dark:text-amber-400" /> Est. CBAM Tax Payable</p>"""
new_dropdown_title = """<p className="text-slate-500 dark:text-slate-400 font-medium flex items-center gap-2"><FileText className="w-4 h-4 text-amber-600 dark:text-amber-400" /> Est. CBAM Tax Payable</p>"""
# Actually let's just change the select options
old_select = """                  <select 
                    value={selectedYear} 
                    onChange={e => setSelectedYear(e.target.value as any)}
                    className="text-xs bg-slate-100 dark:bg-slate-800 border-none rounded p-1 font-bold text-slate-700 dark:text-slate-300 outline-none cursor-pointer max-w-[140px]"
                  >
                    <option value="2034">2034 (100% Gross)</option>
                    <option value="2027">2027 (~5% effective)</option>
                    <option value="2026">2026 (~2.5% effective)</option>
                  </select>"""
new_select = """                  <select 
                    value={selectedYear} 
                    onChange={e => setSelectedYear(e.target.value as any)}
                    className="text-xs bg-slate-100 dark:bg-slate-800 border-none rounded p-1 font-bold text-slate-700 dark:text-slate-300 outline-none cursor-pointer max-w-[160px]"
                  >
                    <option value="2034">If imported in 2034 (100%)</option>
                    <option value="2027">If imported in 2027 (~5%)</option>
                    <option value="2026">If imported in 2026 (~2.5%)</option>
                  </select>"""
code = code.replace(old_select, new_select)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "w", encoding="utf-8") as f:
    f.write(code)

print("Frontend patched.")
