path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AccountModals.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('{profile.tier === "advanced" && (')
print(content[idx:idx+2500])
