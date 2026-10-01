path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AdvancedMaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import Papa from "papaparse";\n', '')
content = content.replace('import * as XLSX from "xlsx";\n', '')
content = content.replace('import { Database, Upload, FileUp, Loader2, AlertCircle, CheckCircle2 } from "lucide-react";', 'import { Database, Loader2, CheckCircle2 } from "lucide-react";')
content = content.replace('  const fileInputRef = useRef<HTMLInputElement>(null);\n', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Unused imports removed!")
