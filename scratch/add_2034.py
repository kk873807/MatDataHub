import sys
content = open('next-frontend/src/app/analytics/cbam/page.tsx', 'r', encoding='utf-8').read()

old = '<h3 className="text-3xl font-bold text-amber-500">€{estimatedTaxEUR.toLocaleString(undefined, { maximumFractionDigits: 2 })}</h3>'
new = '''<h3 className="text-3xl font-bold text-amber-500">€{estimatedTaxEUR.toLocaleString(undefined, { maximumFractionDigits: 2 })}</h3>
                  <div className="bg-amber-50 dark:bg-amber-900/20 px-2 py-1 rounded inline-block mt-1 border border-amber-100 dark:border-amber-800/50">
                    <p className="text-xs text-amber-700 dark:text-amber-400 font-medium">Ref 2034 (100%): €{(taxableTonnes * 75.0).toLocaleString(undefined, { maximumFractionDigits: 2 })}</p>
                  </div>'''
if old in content:
    with open('next-frontend/src/app/analytics/cbam/page.tsx', 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))
    print('Added 2034 ref')
else:
    print('Not found')
