import sys
import re
with open('app/workflows.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Revert de minimis
old_deminimis = """            is_deminimis_eligible = "NO"
            is_exempt = "Origin is exempt" in " | ".join(notes) or "Destination outside EU" in " | ".join(notes)
            
            is_elec_or_hydro = False
            if clean_cn:
                if clean_cn.startswith('2716'):
                    is_elec_or_hydro = True
                    notes.append("De minimis exemption does not apply to Electricity")
                elif clean_cn.startswith('2804'):
                    is_elec_or_hydro = True
                    notes.append("De minimis exemption does not apply to Hydrogen")
            
            if not is_elec_or_hydro:
                if cn_status == "EXACT_MATCH" and sector_lower and any(x in sector_lower for x in ['electric', 'hydrogen']):
                    is_elec_or_hydro = True
                    notes.append(f"De minimis exemption does not apply to {sector_lower.title()}")

            if not is_exempt and not is_elec_or_hydro and not is_out_of_scope and clean_cn:
                is_deminimis_eligible = "YES\""""

new_deminimis = """            is_deminimis_eligible = "NO"
            if cn_status == "EXACT_MATCH" and sector_lower:
                if any(x in sector_lower for x in ['electric', 'hydrogen']):
                    notes.append(f"De minimis exemption does not apply to {sector_lower.title()}")
                elif "Origin is exempt" not in " | ".join(notes) and "Destination outside EU" not in " | ".join(notes):
                    is_deminimis_eligible = "YES\""""

if old_deminimis in content:
    content = content.replace(old_deminimis, new_deminimis)
else:
    print("Could not find old deminimis")

# 2. Revert NOT_COVERED and reject electricity
old_not_covered = """                    if clean_cn.startswith('2716'):
                        errors.append("No default values published for Electricity. Need actual data.")
                        quarantine_reasons.append("Electricity needs actual emissions data")
                    else:
                        # CN code positively identified as not in Annex I
                        is_out_of_scope = True
                        notes.append("CN code is not covered by CBAM Annex I")"""

new_not_covered = """                    # CN code positively identified as not in Annex I
                    is_out_of_scope = True
                    notes.append("CN code is not covered by CBAM Annex I")"""

if old_not_covered in content:
    content = content.replace(old_not_covered, new_not_covered)
else:
    print("Could not find old not covered")

# 3. Reject electricity early based on sector
electricity_rejection = """            if cn_status == "EXACT_MATCH":
                sector_lower = cn_derived_sector
                if 'electric' in sector_lower:
                    errors.append("Electricity must be measured in MWh, not kg. Electricity is unsupported in material BOMs.")
                    quarantine_reasons.append("Unsupported unit: Electricity requires MWh")
                    is_out_of_scope = True
                    notes.append("Electricity skipped (requires MWh unit)")
                sector_valid = True"""

content = content.replace("""            if cn_status == "EXACT_MATCH":
                sector_lower = cn_derived_sector
                sector_valid = True""", electricity_rejection)

with open('app/workflows.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Reverted scope logic and added electricity rejection.")
