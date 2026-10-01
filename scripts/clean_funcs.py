import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AdvancedMaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I want to delete from `const handleFileUpload` all the way down to `return (` (excluding `return (`)
import re
new_content = re.sub(
    r'  const handleFileUpload = async.*?const uploadData = async.*?  return \(',
    '  return (',
    content,
    flags=re.DOTALL
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Removed old functions")
