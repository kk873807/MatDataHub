import os

file_path = 'next-frontend/src/app/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
for i, line in enumerate(lines):
    if 'export default function Home() {' in line:
        out.append(line)
        out.append('  const [currency, setCurrency] = useState<"INR" | "USD" | "EUR">("USD");\n')
        out.append('  const getPrice = (inr: number, usd: string, eur: string) => {\n')
        out.append('    if (currency === "USD") return `$${usd}`;\n')
        out.append('    if (currency === "EUR") return `€${eur}`;\n')
        out.append('    return `₹${inr}`;\n')
        out.append('  };\n')
        continue

    if '<h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4 font-heading">Pay Once. Use Forever. Lifetime Deals.</h2>' in line:
        out.append(line)
        continue

    if '<p className="text-slate-600 dark:text-slate-400">Skip the monthly subscriptions.' in line:
        out.append('          <p className="text-slate-600 dark:text-slate-400">Skip the monthly subscriptions. Grab a lifetime deal before we switch to MRR monthly pricing on <strong>January 1st, 2027</strong>. No credit card required to start free.</p>\n')
        out.append('          \n')
        out.append('          <div className="flex justify-center items-center gap-2 mt-6">\n')
        out.append('             <button onClick={() => setCurrency("USD")} className={`px-4 py-1.5 rounded-full text-sm font-bold transition-all ${currency === "USD" ? "bg-emerald-500 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-slate-700"}`}>USD</button>\n')
        out.append('             <button onClick={() => setCurrency("EUR")} className={`px-4 py-1.5 rounded-full text-sm font-bold transition-all ${currency === "EUR" ? "bg-emerald-500 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-slate-700"}`}>EUR</button>\n')
        out.append('             <button onClick={() => setCurrency("INR")} className={`px-4 py-1.5 rounded-full text-sm font-bold transition-all ${currency === "INR" ? "bg-emerald-500 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-slate-700"}`}>INR</button>\n')
        out.append('          </div>\n')
        continue

    if '<div className="text-4xl font-black text-slate-900 dark:text-white mb-6">₹499<span className="text-sm font-normal text-slate-500"> / lifetime</span></div>' in line:
        out.append('          <div className="text-4xl font-black text-slate-900 dark:text-white mb-6">{getPrice(499, "5.99", "5.49")}<span className="text-sm font-normal text-slate-500"> / lifetime</span></div>\n')
        continue

    if '<div className="text-4xl font-black text-slate-900 dark:text-white mb-6">₹19,999<span className="text-sm font-normal text-slate-500"> / lifetime</span></div>' in line:
        out.append('          <div className="text-4xl font-black text-slate-900 dark:text-white mb-6">{getPrice(19999, "239.00", "219.00")}<span className="text-sm font-normal text-slate-500"> / lifetime</span></div>\n')
        continue

    # Add AI Cap info to Free Tier
    if '<li>Access to compare up to 2 materials</li>' in line:
        out.append(line)
        out.append('              <li><strong>5 Free Lifetime AI Credits</strong></li>\n')
        continue

    # Add Unlimited AI to Advanced Tier
    if '<li>Direct Database API Keys (100 req/min)</li>' in line:
        out.append(line)
        out.append('              <li><strong>Unlimited AI Synthesizer Access</strong></li>\n')
        continue
    
    out.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(out)
