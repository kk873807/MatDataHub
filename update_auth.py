import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\account\page.tsx'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

import re

# We will use regex to find the block
match = re.search(r'if \(!profile\) return \(\s*<div.*?</p>\s*</div>\s*</div>\s*\);', text, re.DOTALL)

if not match:
    print("Could not find the target block")
    exit(1)

old_block = match.group(0)

new_block = """if (!profile) return (
    <div className="fixed inset-0 z-[100] flex bg-slate-950">
      {/* Left Pane - Marketing / Branding */}
      <div className="hidden lg:flex flex-col justify-between w-1/2 p-12 bg-slate-900 relative overflow-hidden border-r border-slate-800">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-[100px] pointer-events-none transform translate-x-1/3 -translate-y-1/3"></div>
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-emerald-600/10 rounded-full blur-[100px] pointer-events-none transform -translate-x-1/3 translate-y-1/3"></div>
        
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-16">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-blue-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Database className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-2xl tracking-tight text-white">MatDataHub</span>
          </div>

          <h1 className="text-4xl lg:text-5xl font-extrabold text-white mb-6 leading-tight">
            Accelerate your <br />
            <span className="text-indigo-400">engineering workflow.</span>
          </h1>
          <p className="text-slate-400 text-lg max-w-md leading-relaxed">
            Join thousands of engineers and researchers using MatDataHub to analyze macroeconomic pricing, CBAM emissions, and multi-objective material substitutions.
          </p>
        </div>

        <div className="relative z-10 bg-slate-950/50 backdrop-blur-md border border-slate-800 p-6 rounded-2xl max-w-lg shadow-2xl">
          <div className="flex gap-4">
            <div className="text-4xl text-indigo-500/30 font-serif">"</div>
            <div>
              <p className="text-slate-300 text-sm leading-relaxed italic mb-4">
                "The unified workflow completely changed how we estimate BOM costs and structural viability in parallel. Absolutely essential platform."
              </p>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-indigo-900 border border-indigo-700 flex items-center justify-center text-xs font-bold text-indigo-300">SJ</div>
                <div>
                  <p className="text-white font-bold text-xs">Dr. Sarah Jenkins</p>
                  <p className="text-slate-500 text-[10px]">Lead Materials Scientist</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Pane - Auth Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 relative overflow-y-auto">
        <div className="w-full max-w-md">
          <div className="lg:hidden flex items-center gap-2 mb-12 justify-center">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-blue-600 flex items-center justify-center">
              <Database className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight text-white">MatDataHub</span>
          </div>

          <div className="mb-10 text-center lg:text-left">
            <h2 className="text-3xl font-bold text-white mb-2">{isLogin ? "Welcome back" : "Create an account"}</h2>
            <p className="text-slate-400">
              {isLogin ? "Enter your details to access your workspace." : "Get started with the Academic Free tier."}
            </p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-rose-900/20 border border-rose-500/30 text-rose-400 text-sm rounded-xl flex items-start gap-3">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <p>{error}</p>
            </div>
          )}

          <form onSubmit={handleAuth} className="space-y-5">
            {!isLogin && (
              <div>
                <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Full Name</label>
                <input name="username" type="text" required={!isLogin} className="w-full bg-slate-900/50 border border-slate-800 rounded-xl p-3.5 text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all placeholder:text-slate-600" placeholder="e.g. John Doe" />
              </div>
            )}
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Work Email</label>
              <input name="email" type="email" required defaultValue={isLogin ? "test@matdatahub.com" : ""} className="w-full bg-slate-900/50 border border-slate-800 rounded-xl p-3.5 text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all placeholder:text-slate-600" placeholder="you@company.com" />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Password</label>
              <input name="password" type="password" required defaultValue={isLogin ? "password123" : ""} className="w-full bg-slate-900/50 border border-slate-800 rounded-xl p-3.5 text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all placeholder:text-slate-600" placeholder="••••••••" />
              {!isLogin && (
                <p className="text-[10px] text-slate-500 mt-2">
                  Must be at least 8 characters containing letters, numbers, and symbols.
                </p>
              )}
            </div>
            {!isLogin && (
              <div>
                <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Confirm Password</label>
                <input name="confirmPassword" type="password" required={!isLogin} className="w-full bg-slate-900/50 border border-slate-800 rounded-xl p-3.5 text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all placeholder:text-slate-600" placeholder="••••••••" />
              </div>
            )}
            <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-indigo-600/20 mt-2 flex justify-center">
              {isLogin ? "Sign In" : "Create Account"}
            </button>
          </form>

          <div className="mt-8">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-800"></div>
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-slate-950 px-3 text-slate-500 font-bold tracking-wider">Or continue with</span>
              </div>
            </div>
            
            <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button 
                type="button" 
                onClick={() => window.location.href = `${API}/auth/google`}
                className="flex items-center justify-center gap-3 bg-slate-900 border border-slate-800 hover:bg-slate-800 hover:border-slate-700 text-white px-4 py-3.5 rounded-xl transition-all"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                <span className="text-sm font-medium">Google</span>
              </button>
              <button 
                type="button" 
                onClick={() => alert("Apple Sign In is coming soon!")}
                className="flex items-center justify-center gap-3 bg-slate-900 border border-slate-800 hover:bg-slate-800 hover:border-slate-700 text-white px-4 py-3.5 rounded-xl transition-all opacity-50 cursor-not-allowed"
              >
                <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.15 2.95.97 3.83 2.32-3.3 1.94-2.76 6.55.61 7.91-.77 1.83-1.63 3.46-3.09 2.78zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/>
                </svg>
                <span className="text-sm font-medium">Apple</span>
              </button>
            </div>
          </div>

          <p className="mt-8 text-center text-sm text-slate-400">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button onClick={() => {setIsLogin(!isLogin); setError("");}} className="text-indigo-400 hover:text-indigo-300 font-semibold hover:underline transition-all">
              {isLogin ? "Register here" : "Sign In"}
            </button>
          </p>
        </div>
      </div>
    </div>
  );"""

new_text = text.replace(old_block, new_block)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_text)
    print("Replaced successfully!")
