import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix Electricity missing in MAP
code = code.replace(
    '"hydrogen": [],',
    '"hydrogen": [],\n        "electricity": [],'
)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Workflows patched with electricity.")
