import re
path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AdvancedMaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_err = '''              if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Failed to upload material");
              }'''

new_err = '''              if (!res.ok) {
                const errData = await res.json();
                let errMsg = "Failed to upload material";
                if (errData.detail) {
                  if (typeof errData.detail === "string") {
                    errMsg = errData.detail;
                  } else if (Array.isArray(errData.detail)) {
                    errMsg = errData.detail.map((e: any) => `${e.loc[e.loc.length-1]}: ${e.msg}`).join(", ");
                  }
                }
                throw new Error(errMsg);
              }'''

if old_err in content:
    content = content.replace(old_err, new_err)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Error handler patched.")
else:
    print("Error handler not found.")
