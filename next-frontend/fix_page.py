import os
filepath = r'src\app\page.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Google OAuth Redirect
text = text.replace(
    'localStorage.setItem("token", oauthToken);\n      window.history.replaceState({}, "", "/");',
    'localStorage.setItem("token", oauthToken);\n      window.location.href = "/dashboard";\n      return;'
)

# Add isLoggedIn button to Hero
hero_btn = '                  {authChecked && !isLoggedIn && (\n                    <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="flex items-center gap-2 px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-indigo-600/20 w-full sm:w-auto justify-center">\n                      Access Platform <ArrowRight className="w-4 h-4" />\n                    </button>\n                  )}'
new_hero_btn = hero_btn + '\n                  {authChecked && isLoggedIn && (\n                    <Link href="/dashboard" className="flex items-center gap-2 px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-indigo-600/20 w-full sm:w-auto justify-center">\n                      Go to Dashboard <ArrowRight className="w-4 h-4" />\n                    </Link>\n                  )}'
text = text.replace(hero_btn, new_hero_btn)

# Fix Pricing buttons
text = text.replace(
    '<button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Start Free</button>',
    '{isLoggedIn ? <Link href="/dashboard" className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Go to Dashboard</Link> : <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Start Free</button>}'
)

text = text.replace(
    '<button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade to Pro</button>',
    '{isLoggedIn ? <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade in Account</Link> : <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade to Pro</button>}'
)

text = text.replace(
    '<button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Get Advanced</button>',
    '{isLoggedIn ? <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Upgrade in Account</Link> : <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Get Advanced</button>}'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
