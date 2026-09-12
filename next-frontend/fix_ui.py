import os
import re

files_to_fix = [
    r'src\app\materials\page.tsx',
    r'src\app\materials\[id]\page.tsx',
    r'src\app\analytics\compare\page.tsx',
    r'src\app\analytics\substitution\page.tsx',
    r'src\app\analytics\synthesizer\page.tsx',
    r'src\app\ai\page.tsx',
    r'src\app\projects\page.tsx',
    r'src\app\projects\[id]\page.tsx',
]

def fix_contrast(text):
    # Fix chat bubbles and markdown renderers which hardcode text-slate-200
    text = re.sub(r'(?<!dark:)text-slate-200\b', r'text-slate-700 dark:text-slate-200', text)
    text = re.sub(r'(?<!dark:)text-slate-300\b', r'text-slate-600 dark:text-slate-300', text)
    
    # Border issues like border-emerald-900 in light mode
    text = re.sub(r'(?<!dark:)border-emerald-900\b', r'border-emerald-200 dark:border-emerald-900', text)
    text = re.sub(r'(?<!dark:)border-slate-600\b', r'border-slate-300 dark:border-slate-600', text)
    text = re.sub(r'(?<!dark:)border-slate-700\b', r'border-slate-200 dark:border-slate-700', text)
    
    # Background issues
    text = re.sub(r'(?<!dark:)bg-slate-700\b', r'bg-slate-100 dark:bg-slate-700', text)
    text = re.sub(r'(?<!dark:)bg-slate-800\b', r'bg-slate-100 dark:bg-slate-800', text)
    
    # Dark texts without dark equivalents
    text = re.sub(r'(?<!dark:)text-slate-500\b(?! dark:)', r'text-slate-500 dark:text-slate-400', text)
    
    # Cleanup any accidental duplications (e.g. text-slate-700 dark:text-slate-700 dark:text-slate-200)
    text = text.replace('dark:text-slate-700 dark:text-slate-200', 'dark:text-slate-200')
    text = text.replace('dark:text-slate-600 dark:text-slate-300', 'dark:text-slate-300')
    text = text.replace('dark:text-slate-500 dark:text-slate-400', 'dark:text-slate-400')
    
    # Fix the weird "bg-red-100 dark:bg-red-100 dark:bg-red-900/30" created by previous bad script
    text = re.sub(r'bg-([a-z]+)-100 dark:bg-\1-100 dark:bg-\1-900', r'bg-\1-100 dark:bg-\1-900', text)
    text = re.sub(r'bg-([a-z]+)-100 dark:bg-\1-100\b', r'bg-\1-100', text)
    
    return text

for file_path in files_to_fix:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, does not exist.")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = fix_contrast(content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {file_path}")
    else:
        print(f"No changes needed for {file_path}")
