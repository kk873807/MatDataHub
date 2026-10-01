import re
path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AdvancedMaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import { useState, useRef } from "react";', 'import { useState, useRef, useEffect } from "react";')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Import fixed!")
