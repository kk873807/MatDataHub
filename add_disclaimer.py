import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\materials\[id]\page.tsx'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = "Price Tracking (12M)\n              </h3>"

replacement = """Price Tracking (12M)
              </h3>
              <p className=\"text-[11px] leading-relaxed text-slate-400 mb-6 flex items-start gap-1.5\">
                <Info className=\"w-4 h-4 shrink-0 mt-0.5\" /> Data is generated via macroeconomic proxy indexing for trend analysis. It is not a live spot-price. Please consult a supplier for exact procurement pricing.
              </p>"""

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully")
else:
    print("Target not found")
