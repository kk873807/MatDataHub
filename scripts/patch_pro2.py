import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\AccountModals.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''                      <button onClick={(e) => { e.preventDefault(); e.stopPropagation(); generateApiKeys(); }} className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-colors flex items-center gap-2 relative z-10 cursor-pointer">
                        <Key className="w-4 h-4" /> Generate API Keys
                      </button>
                    )}
                  </div>
                  
                  {/* Custom Materials Manager */}
                  <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
                    <AdvancedMaterialManager />
                  </div>
                </div>
              )}'''

new_code = '''                      <button onClick={(e) => { e.preventDefault(); e.stopPropagation(); generateApiKeys(); }} className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-colors flex items-center gap-2 relative z-10 cursor-pointer">
                        <Key className="w-4 h-4" /> Generate API Keys
                      </button>
                    )}
                  </div>
                </div>
              )}

              {/* Custom Materials (Advanced & Pro) */}
              {(profile.tier === "advanced" || profile.tier === "pro") && (
                <div className="mt-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
                  <AdvancedMaterialManager />
                </div>
              )}'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched AccountModals.tsx")
else:
    print("Could not find the block to patch")
