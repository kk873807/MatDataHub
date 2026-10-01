import re

files = [
    r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AccountModals.tsx',
    r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\account\page.tsx',
    r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\page.tsx'
]

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace the small /mo spans
    content = re.sub(r'<span[^>]*>/mo</span>', '<span className="text-sm font-medium text-slate-500 dark:text-slate-400">/lifetime</span>', content)
    
    # Replace button texts
    content = content.replace('Pay &#8377;499/mo & Upgrade', 'Pay &#8377;499 for Lifetime PRO')
    content = content.replace('Pay &#8377;19,999/mo & Upgrade', 'Pay &#8377;19,999 for Lifetime ADVANCED')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated all pricing to Lifetime!")
