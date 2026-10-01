import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

old_factors = """FALLBACK_CARBON_FACTORS = {
    "stainless steel": 6.15, "carbon steel": 2.10, "steel": 2.10,
    "aluminium": 8.24, "aluminum": 8.24,
    "copper": 3.81, "brass": 3.50, "bronze": 3.70,
    "titanium": 35.7, "nickel": 12.4, "zinc": 3.86,
    "magnesium": 8.10, "iron": 2.10, "cast iron": 2.10,
    "lead": 1.57, "tin": 14.5,
    "nylon": 8.50, "polyethylene": 1.94, "polypropylene": 1.95,
    "pvc": 2.41, "polycarbonate": 7.62, "abs": 3.76,
    "epoxy": 6.70, "polyester": 2.70, "rubber": 3.18,
    "ptfe": 10.2, "peek": 26.4, "polymer": 3.40, "plastic": 3.40,
    "concrete": 0.15, "cement": 0.95, "glass": 1.10, "ceramic": 1.20,
    "carbon fiber": 32.5, "fiberglass": 8.10, "composite": 5.50,
    "wood": 0.10, "paper": 0.90, "cardboard": 0.85,
    "hydrogen": 10.4, "fertiliser": 3.0, "fertilizer": 3.0,
    "water": 0.001, "air": 0.0, "gas": 0.0, "oil": 3.0, "lubricant": 3.2
}"""

new_factors = """FALLBACK_CARBON_FACTORS = {
    "hydrogen": 10.4, "ammonia": 2.82,
    "stainless steel": 2.21, "carbon steel": 2.01, "steel": 2.01,
    "aluminium": 2.36, "aluminum": 2.36,
    "copper": 3.81, "brass": 3.50, "bronze": 3.70,
    "titanium": 35.7, "nickel": 12.4, "zinc": 3.86,
    "magnesium": 8.10, "iron": 2.01, "cast iron": 2.01,
    "lead": 1.57, "tin": 14.5,
    "nylon": 8.50, "polyethylene": 1.94, "polypropylene": 1.95,
    "pvc": 2.41, "polycarbonate": 7.62, "abs": 3.76,
    "epoxy": 6.70, "polyester": 2.70, "rubber": 3.18,
    "ptfe": 10.2, "peek": 26.4, "polymer": 3.40, "plastic": 3.40,
    "concrete": 0.15, "cement": 0.87, "glass": 1.10, "ceramic": 1.20,
    "carbon fiber": 32.5, "fiberglass": 8.10, "composite": 5.50,
    "wood": 0.10, "paper": 0.90, "cardboard": 0.85,
    "fertiliser": 3.0, "fertilizer": 3.0,
    "water": 0.001, "air": 0.0, "gas": 0.0, "oil": 3.0, "lubricant": 3.2
}"""
code = code.replace(old_factors, new_factors)

old_dq = """            data_quality = extract_string(['data_quality', 'data quality'])
            if not data_quality:
                errors.append("Missing data quality")
            elif data_quality.lower() not in ('verified', 'default', 'estimated', 'measured'):
                errors.append("Invalid data quality")
            elif data_quality.lower() == 'verified' and price_paid_val is None:
                errors.append("Missing carbon price for Verified data")"""
new_dq = """            data_quality = extract_string(['data_quality', 'data quality'])
            if not data_quality:
                errors.append("Missing data quality")
            else:
                dq_lower = data_quality.lower()
                if not any(x in dq_lower for x in ['verified', 'default', 'estimated', 'measured']):
                    errors.append("Invalid data quality")
                elif 'verified' in dq_lower and price_paid_val is None:
                    errors.append("Missing carbon price for Verified data")"""
code = code.replace(old_dq, new_dq)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Remaining patches done")
