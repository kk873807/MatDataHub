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

# 1. Update direct_em/indirect_em logic and plausibility checks
old_em_logic = """            direct_em = extract_float(['direct_emissions', 'direct emissions'], 'direct emissions')
            indirect_em = extract_float(['indirect_emissions', 'indirect emissions'], 'indirect emissions')
            
            if direct_em is not None and direct_em > 50.0:
                quarantine_reasons.append("Emissions exceed plausibility bound (50 t/t)")
            if indirect_em is not None and indirect_em > 50.0:
                quarantine_reasons.append("Emissions exceed plausibility bound (50 t/t)")"""

new_em_logic = """            direct_em = extract_float(['direct_emissions', 'direct emissions'], 'direct emissions')
            if direct_em is not None and direct_em < 0:
                errors.append("Direct emissions cannot be negative")
                direct_em = 0.0

            indirect_em = extract_float(['indirect_emissions', 'indirect emissions'], 'indirect emissions')
            if indirect_em is not None and indirect_em < 0:
                errors.append("Indirect emissions cannot be negative")
                indirect_em = 0.0"""
code = code.replace(old_em_logic, new_em_logic)


# 2. Update includes_indirect and plausibility logic
old_includes_indirect = """            provided_carbon_factor = None
            includes_indirect = False
            if allowed_cats is not None:
                if any(k in sector_lower for k in ['cement', 'fertili']):
                    includes_indirect = True
            
            if direct_em is not None:
                provided_carbon_factor = direct_em
                if includes_indirect and indirect_em is not None:
                    provided_carbon_factor += indirect_em
                elif not includes_indirect and indirect_em is not None:
                    notes.append("Indirect emissions excluded for this sector (CBAM definitive rules)")"""

new_includes_indirect = """            provided_carbon_factor = None
            includes_indirect = False
            if allowed_cats is not None:
                if any(k in sector_lower for k in ['cement', 'fertili']):
                    includes_indirect = True
            
            if direct_em is not None and direct_em > 50.0:
                quarantine_reasons.append("Emissions exceed plausibility bound (50 t/t)")
                
            if includes_indirect and indirect_em is not None and indirect_em > 50.0:
                quarantine_reasons.append("Emissions exceed plausibility bound (50 t/t)")
            
            if direct_em is not None:
                provided_carbon_factor = direct_em
                if includes_indirect:
                    if indirect_em is not None:
                        provided_carbon_factor += indirect_em
                    else:
                        errors.append("Missing indirect emissions (using fallback default for total)")
                        provided_carbon_factor = None # Invalidate so it uses full db/fallback factor
                elif not includes_indirect and indirect_em is not None:
                    notes.append("Indirect emissions excluded for this sector (CBAM definitive rules)")"""
code = code.replace(old_includes_indirect, new_includes_indirect)


# 3. Destination EU_DESTINATION_COUNTRIES fix
old_dest = """                invalid_countries = ['nowhereland', 'atlantis', 'narnia', 'test', 'unknown']
                if len(d_lower) < 2 or d_lower in invalid_countries:
                    errors.append("Unrecognized destination country")
                    quarantine_reasons.append("Unrecognized destination country")
                elif d_lower not in self.EU_EEA_COUNTRIES:
                    notes.append("Destination outside EU (exempt)")"""

new_dest = """                invalid_countries = ['nowhereland', 'atlantis', 'narnia', 'test', 'unknown']
                if len(d_lower) < 2 or d_lower in invalid_countries:
                    errors.append("Unrecognized destination country")
                    quarantine_reasons.append("Unrecognized destination country")
                elif d_lower not in self.EU_DESTINATION_COUNTRIES:
                    notes.append("Destination outside EU (exempt)")"""
code = code.replace(old_dest, new_dest)


# 4. Cement CN logic
old_cement_cn = """                elif "cement" in sector_lower:
                    if not clean_cn.startswith("2523"):
                        errors.append("CN Code does not match Cement sector")
                        quarantine_reasons.append("CN Code does not match Cement sector")"""

new_cement_cn = """                elif "cement" in sector_lower:
                    if not clean_cn.startswith(("2523", "2507")):
                        errors.append("CN Code does not match Cement sector")
                        quarantine_reasons.append("CN Code does not match Cement sector")"""
code = code.replace(old_cement_cn, new_cement_cn)


# 5. Data Quality ESG penalty
old_dq_esg = """                supp_score = min(supplier_risk / 100.0 * 20, 20)
                lead_score = 10 if lead_time and lead_time > 180 else (5 if lead_time and lead_time > 90 else 0)
                base_esg = carbon_score + geo_score + ss_score + supp_score + lead_score"""

new_dq_esg = """                supp_score = min(supplier_risk / 100.0 * 20, 20)
                lead_score = 10 if lead_time and lead_time > 180 else (5 if lead_time and lead_time > 90 else 0)
                dq_score = 0
                if data_quality:
                    if 'default' in data_quality.lower() or 'unknown' in data_quality.lower():
                        dq_score = 10
                    elif 'estimated' in data_quality.lower():
                        dq_score = 5
                base_esg = carbon_score + geo_score + ss_score + supp_score + lead_score + dq_score"""
code = code.replace(old_dq_esg, new_dq_esg)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Backend patched successfully.")
