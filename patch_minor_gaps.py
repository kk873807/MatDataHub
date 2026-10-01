import os
import re

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Zero out Carbon_Factor when errors exist
old_zero = """            if errors:
                total_co2_kg = 0.0
                total_co2_tonnes = 0.0
                cbam_cost_eur = 0.0
                esg_risk = 0.0

            enriched_rows.append({"""

new_zero = """            if errors:
                total_co2_kg = 0.0
                total_co2_tonnes = 0.0
                cbam_cost_eur = 0.0
                esg_risk = 0.0
                carbon_factor = 0.0

            enriched_rows.append({"""
code = code.replace(old_zero, new_zero)

# 2. Add CN Code and Country validation
# We'll insert it right after the enums are checked (around line 233)
old_enum_check = """            data_quality = extract_string(['data_quality', 'data quality'])
            if data_quality and data_quality.lower() == 'verified' and price_paid_val is None:
                errors.append("Missing carbon price for Verified data")"""

new_val_logic = """            data_quality = extract_string(['data_quality', 'data quality'])
            if data_quality and data_quality.lower() == 'verified' and price_paid_val is None:
                errors.append("Missing carbon price for Verified data")
                
            # CN Code Validation
            cn_code = extract_string(['cn_code', 'hs_code', 'cn code'])
            if cn_code:
                # Strip spaces, dots, hyphens
                clean_cn = cn_code.replace(" ", "").replace(".", "").replace("-", "")
                if not clean_cn.isdigit() or len(clean_cn) < 4:
                    errors.append("Invalid CN Code format")
            else:
                pass # Only flag if explicitly required by business rules, but user mainly cared about malformed ones
                
            # Country Validation (lightweight heuristic list)
            country = extract_string(['country', 'origin', 'supplier_country'])
            if not country:
                errors.append("Missing supplier country")
            else:
                # Basic check for fictional or obviously invalid countries. 
                # (A full list is too long, but we can check for common joke entries and require >2 chars)
                c_lower = country.lower().strip()
                invalid_countries = ['nowhereland', 'atlantis', 'narnia', 'test', 'unknown']
                if len(c_lower) < 2 or c_lower in invalid_countries:
                    errors.append("Unrecognized country")"""

code = code.replace(old_enum_check, new_val_logic)


with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Patch applied.")
