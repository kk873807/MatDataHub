import os
import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\page.tsx'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the free pricing text and symbol
text = re.sub(r'\{.*"Search 100\+ basic materials".*?\]\.map', 
              '{["Search limited basic materials", "View mechanical properties", "Basic AI Adviser access", "Community Support"].map', text)

# Fix the symbols using HTML entity for Rupee
text = re.sub(r'<div className="text-4xl font-extrabold text-white mb-8">.*?</mo></span></div>', '', text) # will manually replace below

# It's better to just replace the specific blocks.
# Let's replace the whole grid block for pricing.

start_str = '<div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">'
end_str = '</div>\n        </div>\n      </section>\n\n      {/* Footer */}'

if start_str in text and end_str in text:
    before = text.split(start_str)[0]
    after = text.split(end_str)[1]
    
    new_grid = """<div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            
            {/* Free */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 flex flex-col">
              <h3 className="text-xl font-bold text-white mb-2">Academic Free</h3>
              <p className="text-slate-400 text-sm mb-6 h-10">Perfect for students and open research.</p>
              <div className="text-4xl font-extrabold text-white mb-8">&#8377;0<span className="text-lg font-medium text-slate-500">/mo</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Search limited basic materials", "View mechanical properties", "Basic AI Adviser", "Community Support"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" /> {f}
                  </li>
                ))}
              </ul>
              <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-colors">Start Free</Link>
            </div>

            {/* Pro */}
            <div className="bg-slate-900 border-2 border-indigo-500 rounded-2xl p-8 flex flex-col relative transform md:-translate-y-4 shadow-2xl shadow-indigo-900/20">
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-indigo-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Most Popular</div>
              <h3 className="text-xl font-bold text-white mb-2">Professional</h3>
              <p className="text-slate-400 text-sm mb-6 h-10">For independent engineers and small firms.</p>
              <div className="text-4xl font-extrabold text-white mb-8">&#8377;499<span className="text-lg font-medium text-slate-500">/mo</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Full 1000+ material database", "Export detailed PDFs", "Advanced AI Adviser", "Unlimited Workspaces"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-indigo-400" /> {f}
                  </li>
                ))}
              </ul>
              <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade to Pro</Link>
            </div>

            {/* Advanced */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 flex flex-col">
              <h3 className="text-xl font-bold text-white mb-2">Advanced Enterprise</h3>
              <p className="text-slate-400 text-sm mb-6 h-10">Full financial & physics capabilities.</p>
              <div className="text-4xl font-extrabold text-white mb-8">&#8377;19,999<span className="text-lg font-medium text-slate-500">/mo</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Macroeconomic Proxy Pricing", "CBAM Emissions Calculator", "Engineering Physics Tools", "Composite Synthesizer", "Priority API Access"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-amber-500" /> {f}
                  </li>
                ))}
              </ul>
              <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-colors">Get Advanced</Link>
            </div>

          """
    
    text = before + start_str + new_grid + end_str + after
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Pricing updated")
else:
    print("Pricing section not found")
