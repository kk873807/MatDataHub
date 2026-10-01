import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AdvancedMaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the Bulk Upload section entirely
content = re.sub(
    r'<div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-6">.*?Bulk Upload Materials.*?</div>\s*<div className="bg-slate-50', 
    '<div className="bg-slate-50', 
    content, 
    flags=re.DOTALL
)

# Add source_url input to the form
old_inputs = '<input type="text" name="category" placeholder="Category (Required)" required className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />'
new_inputs = old_inputs + '\n              <input type="url" name="source_url" placeholder="Source URL (Required)" required className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />'

content = content.replace(old_inputs, new_inputs)

# Update form handler to preserve source_url as string
old_condition = 'key === "name" || key === "category" || key === "subcategory" || key === "description" || key === "standard" || key === "grade"'
new_condition = 'key === "name" || key === "category" || key === "subcategory" || key === "description" || key === "standard" || key === "grade" || key === "source_url"'
content = content.replace(old_condition, new_condition)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('AdvancedMaterialManager.tsx updated')
