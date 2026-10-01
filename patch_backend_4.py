import os

def replace_between(text, start_str, end_str, replacement):
    start_idx = text.find(start_str)
    if start_idx == -1: return text
    end_idx = text.find(end_str, start_idx)
    if end_idx == -1: return text
    end_idx += len(end_str)
    return text[:start_idx] + replacement + text[end_idx:]

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Fallback Factors
old_factors = """FALLBACK_CARBON_FACTORS = {
    "stainless steel": 6.15, "carbon steel": 1.85, "steel": 1.85,
    "aluminium": 8.24, "aluminum": 8.24,
    "copper": 3.81, "brass": 3.50, "bronze": 3.70,
    "titanium": 35.7, "nickel": 12.4, "zinc": 3.86,
    "magnesium": 8.10, "iron": 1.91, "cast iron": 1.91,
    "lead": 1.57, "tin": 14.5,
    "nylon": 8.50, "polyethylene": 1.94, "polypropylene": 1.95,
    "pvc": 2.41, "polycarbonate": 7.62, "abs": 3.76,
    "epoxy": 6.70, "polyester": 2.70, "rubber": 3.18,
    "ptfe": 10.2, "peek": 26.4, "polymer": 3.40, "plastic": 3.40,
    "concrete": 0.15, "cement": 0.95, "glass": 1.10, "ceramic": 1.20,
    "carbon fiber": 32.5, "fiberglass": 8.10, "composite": 5.50,
    "wood": 0.10, "paper": 0.90, "cardboard": 0.85,
    "water": 0.001, "air": 0.0, "gas": 0.0, "oil": 3.0, "lubricant": 3.2
}"""

new_factors = """FALLBACK_CARBON_FACTORS = {
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
code = code.replace(old_factors, new_factors)

# 2. Add validation flags for missing risk/data fields
old_risk_checks = """            supplier_risk = extract_float(['supplier_risk', 'vendor_risk'], 'supplier risk') or 0.0
            if supplier_risk > 100:
                errors.append("Risk score capped at 100")
                supplier_risk = 100.0
            if supplier_risk < 0:
                errors.append("Risk score must be positive")
                supplier_risk = 0.0
                
            lead_time = extract_float(['lead_time', 'lead time'], None)
            if lead_time is not None and (lead_time < 0 or lead_time > 3650):
                errors.append("Lead time out of plausible bounds")

            single_source = extract_string(['single_source', 'sole_source'])
            if single_source and single_source.lower() not in ('yes', 'no', 'true', 'false', 'y', 'n'):
                errors.append("Invalid single_source_flag")
            geo_risk = extract_string(['geopolitical', 'geo_risk', 'country_risk'])
            if geo_risk and geo_risk.lower() not in ('low', 'medium', 'high'):
                errors.append("Invalid geopolitical_risk")
            data_quality = extract_string(['data_quality', 'data quality'])
            if data_quality and data_quality.lower() == 'verified' and price_paid_val is None:
                errors.append("Missing carbon price for Verified data")"""

new_risk_checks = """            supplier_name = extract_string(['supplier_name', 'supplier', 'vendor'])
            if not supplier_name:
                errors.append("Missing supplier name")

            supplier_risk = extract_float(['supplier_risk', 'vendor_risk'], 'supplier risk') or 0.0
            if supplier_risk > 100:
                errors.append("Risk score capped at 100")
                supplier_risk = 100.0
            if supplier_risk < 0:
                errors.append("Risk score must be positive")
                supplier_risk = 0.0
                
            lead_time = extract_float(['lead_time', 'lead time'], None)
            if lead_time is None:
                errors.append("Missing lead time")
            elif lead_time < 0 or lead_time > 3650:
                errors.append("Lead time out of plausible bounds")

            single_source = extract_string(['single_source', 'sole_source'])
            if not single_source:
                errors.append("Missing single_source_flag")
            elif single_source.lower() not in ('yes', 'no', 'true', 'false', 'y', 'n'):
                errors.append("Invalid single_source_flag")
                
            geo_risk = extract_string(['geopolitical', 'geo_risk', 'country_risk'])
            if not geo_risk:
                errors.append("Missing geopolitical_risk")
            elif geo_risk.lower() not in ('low', 'medium', 'high'):
                errors.append("Invalid geopolitical_risk")
                
            data_quality = extract_string(['data_quality', 'data quality'])
            if not data_quality:
                errors.append("Missing data quality")
            elif data_quality.lower() not in ('verified', 'default', 'estimated', 'measured'):
                errors.append("Invalid data quality")
            elif data_quality.lower() == 'verified' and price_paid_val is None:
                errors.append("Missing carbon price for Verified data")"""
code = code.replace(old_risk_checks, new_risk_checks)

# 3. Add CN Code missing check
old_cn = """            cn_code = extract_string(['cn_code', 'hs_code', 'cn code'])
            clean_cn = ""
            if cn_code:
                clean_cn = cn_code.replace(" ", "").replace(".", "").replace("-", "")
                if not clean_cn.isdigit() or len(clean_cn) < 4:
                    errors.append("Invalid CN Code format")
                    quarantine_reasons.append("Invalid CN Code format")"""

new_cn = """            cn_code = extract_string(['cn_code', 'hs_code', 'cn code'])
            clean_cn = ""
            if not cn_code:
                errors.append("Missing CN Code")
            else:
                clean_cn = cn_code.replace(" ", "").replace(".", "").replace("-", "")
                if not clean_cn.isdigit() or len(clean_cn) < 4:
                    errors.append("Invalid CN Code format")
                    quarantine_reasons.append("Invalid CN Code format")"""
code = code.replace(old_cn, new_cn)

# 4. Enforce pre-2026 tax zeroing and ESG Lead Time
old_esg_tax = """            net_cbam_price = max(CBAM_REFERENCE_PRICE_EUR - price_paid, 0.0)
            
            is_exempt = False
            if "Origin is exempt from CBAM (EU/EEA)" in notes or "Destination outside EU (exempt)" in notes:
                is_exempt = True
            
            cbam_cost_eur = round(total_co2_tonnes * net_cbam_price, 2) if sector_valid and not is_exempt else 0.0
            
            carbon_score = min(carbon_factor / 30.0 * 50, 50)
            if geo_risk or single_source or supplier_risk > 0:
                geo_score = 15 if geo_risk and "high" in geo_risk.lower() else (7.5 if geo_risk and "med" in geo_risk.lower() else 0)
                ss_score = 15 if single_source and ("yes" in single_source.lower() or "true" in single_source.lower() or "y" == single_source.lower()) else 0
                supp_score = min(supplier_risk / 100.0 * 20, 20)
                base_esg = carbon_score + geo_score + ss_score + supp_score
            else:"""

new_esg_tax = """            net_cbam_price = max(CBAM_REFERENCE_PRICE_EUR - price_paid, 0.0)
            
            is_exempt = False
            if "Origin is exempt from CBAM (EU/EEA)" in notes or "Destination outside EU (exempt)" in notes or "Pre-2026 shipment (reporting-only phase, no financial liability)" in notes:
                is_exempt = True
            
            cbam_cost_eur = round(total_co2_tonnes * net_cbam_price, 2) if sector_valid and not is_exempt else 0.0
            
            carbon_score = min(carbon_factor / 30.0 * 50, 50)
            if geo_risk or single_source or supplier_risk > 0:
                geo_score = 15 if geo_risk and "high" in geo_risk.lower() else (7.5 if geo_risk and "med" in geo_risk.lower() else 0)
                ss_score = 15 if single_source and ("yes" in single_source.lower() or "true" in single_source.lower() or "y" == single_source.lower()) else 0
                supp_score = min(supplier_risk / 100.0 * 20, 20)
                lead_score = 10 if lead_time and lead_time > 180 else (5 if lead_time and lead_time > 90 else 0)
                base_esg = carbon_score + geo_score + ss_score + supp_score + lead_score
            else:"""
code = code.replace(old_esg_tax, new_esg_tax)

# 5. Fix Validation_Errors combining errors + quarantine_reasons
old_validation_out = """                "Validation_Errors": " | ".join(errors) if errors else "None",
                "Included_In_Total": included_str"""

new_validation_out = """                "Validation_Errors": " | ".join(list(dict.fromkeys(errors + quarantine_reasons))) if (errors or quarantine_reasons) else "None",
                "Included_In_Total": included_str"""
code = code.replace(old_validation_out, new_validation_out)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Backend patched successfully.")
