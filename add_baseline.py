import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\materials\[id]\page.tsx'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = "                <span className=\"text-xl text-slate-500 font-medium\">/kg</span>\n              </p>\n              {priceHistory.length > 0 && ("

replacement = "                <span className=\"text-xl text-slate-500 font-medium\">/kg</span>\n              </p>\n              <p className=\"text-[10px] text-slate-500 mb-2 mt-[-4px] uppercase tracking-wide font-bold\">Estimated Baseline</p>\n              {priceHistory.length > 0 && ("

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully")
else:
    print("Target not found")
