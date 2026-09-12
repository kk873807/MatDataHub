import os

with open('src/app/contact/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Change grid-cols-3 to grid-cols-2
code = code.replace('grid lg:grid-cols-3 gap-8', 'grid md:grid-cols-2 gap-8 max-w-4xl mx-auto')

# Remove the Office card block
office_block = '''        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-3xl hover:shadow-xl hover:shadow-blue-900/5 transition-all text-center flex flex-col items-center">
          <div className="w-14 h-14 bg-violet-100 dark:bg-violet-900/30 rounded-2xl flex items-center justify-center mb-6">
            <MapPin className="w-7 h-7 text-violet-600 dark:text-violet-400" />
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">Office</h3>
          <p className="text-slate-500 dark:text-slate-400 text-sm mb-6 flex-1">MatDataHub HQ<br/>Innovation Park, Phase 1</p>
          <span className="font-bold text-violet-600 dark:text-violet-400">View on Map</span>
        </div>'''

code = code.replace(office_block, '')

with open('src/app/contact/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed contact page")
