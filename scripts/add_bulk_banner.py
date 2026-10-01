import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AdvancedMaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Mail to imports
if 'Mail' not in content:
    content = content.replace('import { Database, Loader2, CheckCircle2 }', 'import { Database, Loader2, CheckCircle2, Mail, Info }')

# 2. Add the banner
old_ui = '''      <div className="p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">'''

new_ui = '''      <div className="p-6">
        
        {/* Bulk Upload Notice */}
        <div className="mb-8 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800/50 rounded-xl p-4 flex items-start gap-3">
          <Info className="w-5 h-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
          <div>
            <h3 className="text-indigo-900 dark:text-indigo-300 font-semibold text-sm">Want to add materials in bulk?</h3>
            <p className="text-indigo-700 dark:text-indigo-400 text-xs mt-1 leading-relaxed">
              To ensure data integrity, bulk uploading is handled by our team. If you have a large dataset, please contact us at <a href="mailto:matdatahub.support@gmail.com" className="font-bold underline hover:text-indigo-800 dark:hover:text-indigo-300">matdatahub.support@gmail.com</a>. 
              Attach your CSV/Excel file along with authentic primary sources (PDFs, source links, or spec sheets) for verification.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">'''

if old_ui in content:
    content = content.replace(old_ui, new_ui)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added bulk upload banner")
else:
    print("UI block not found")
