import os
import re

with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# The exact target string:
#                   {isLanding ? (
#                     <Link href="/dashboard" className="text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 px-5 py-2.5 rounded-full transition-all shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40">
#                       Go to App
#                     </Link>
#                   ) : (
#                     <Link href="/account" className="flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
#                       <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center text-white font-bold text-xs">
#                         {userInfo?.name.charAt(0).toUpperCase() || "U"}
#                       </div>
#                       <span className={inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border \}>
#                         {tierLabel}
#                       </span>
#                     </Link>
#                   )}

# Find the start and end of this block
pattern = r'\{isLanding \? \([\s\S]*?</Link>\s*\)\s*:\s*\([\s\S]*?</Link>\s*\)\}'

new_block = '''{isLanding ? (
                    <Link href="/dashboard" className="text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 px-5 py-2.5 rounded-full transition-all shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40">
                      Go to App
                    </Link>
                  ) : (
                    <div className="relative group">
                      <button className="flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center text-white font-bold text-xs">
                          {userInfo?.name.charAt(0).toUpperCase() || "U"}
                        </div>
                        <span className={inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border }>
                          {tierLabel}
                        </span>
                        <ChevronDown className="w-3 h-3 text-slate-400" />
                      </button>
                      
                      <div className="absolute top-full right-0 mt-2 w-56 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all flex flex-col p-2 z-50">
                        <div className="px-3 py-2 mb-2 border-b border-slate-100 dark:border-slate-800">
                          <p className="text-sm font-bold text-slate-900 dark:text-white truncate">{userInfo?.name || "User"}</p>
                          <p className="text-xs text-slate-500 dark:text-slate-400">{tierLabel} Plan</p>
                        </div>
                        <Link href="/account" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                          <Settings className="w-4 h-4" /> Account Management
                        </Link>
                        <Link href="/account?tab=billing" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                          <CreditCard className="w-4 h-4" /> Transactions & Billing
                        </Link>
                        <Link href="/faq" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                          <LifeBuoy className="w-4 h-4" /> Help Centre & Legal
                        </Link>
                        <button onClick={() => alert('Keyboard shortcuts: \\nCtrl+K: Search\\nCtrl+/: Shortcuts')} className="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors text-left">
                          <Keyboard className="w-4 h-4" /> Keyboard Shortcuts
                        </button>
                        <div className="h-px bg-slate-100 dark:bg-slate-800 my-1"></div>
                        <button onClick={handleLogout} className="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-colors text-left">
                          <LogOut className="w-4 h-4" /> Sign Out
                        </button>
                      </div>
                    </div>
                  )}'''

code = re.sub(pattern, new_block, code, flags=re.DOTALL)

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Replaced auth block!")
