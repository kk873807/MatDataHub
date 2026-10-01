import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

old_sector_logic = """            else:
                sector_valid = False
                if cbam_sector: critical_errors.append("Sector not covered by CBAM")"""

new_sector_logic = """            else:
                sector_valid = True
                if cbam_sector: 
                    critical_errors.append("Sector not covered by CBAM")
                    sector_valid = False"""

code = code.replace(old_sector_logic, new_sector_logic)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Fixed sector_valid default logic.")
