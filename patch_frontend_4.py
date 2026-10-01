import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "r", encoding="utf-8") as f:
    code = f.read()

old_label = """{((totalCO2/1000) - taxableTonnes).toLocaleString(undefined, { maximumFractionDigits: 1 })} t-equivalent excluded (exempt origin/dest or carbon price paid)"""
new_label = """{((totalCO2/1000) - taxableTonnes).toLocaleString(undefined, { maximumFractionDigits: 1 })} t-equivalent excluded (exempt origin/dest, pre-2026, or carbon price paid)"""
code = code.replace(old_label, new_label)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "w", encoding="utf-8") as f:
    f.write(code)

print("Frontend patched.")
