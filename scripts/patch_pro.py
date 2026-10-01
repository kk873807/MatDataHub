import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\account\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''                        }}\n                      >\n                        <Key className="w-4 h-4" /> Generate API Keys\n                      </button>\n                    </div>\n                  )}\n                </div>\n                <AdvancedMaterialManager />\n              </div>\n            )}'''

new_code = '''                        }}\n                      >\n                        <Key className="w-4 h-4" /> Generate API Keys\n                      </button>\n                    </div>\n                  )}\n                </div>\n              </div>\n            )}\n\n            {/* Custom Materials (Advanced & Pro) */}\n            {(profile.tier === "advanced" || profile.tier === "pro") && (\n              <div className="mt-8">\n                <AdvancedMaterialManager />\n              </div>\n            )}'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched account/page.tsx")
else:
    print("Could not find the block to patch")
