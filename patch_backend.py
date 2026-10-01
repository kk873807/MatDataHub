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

# 1. Add Pre-2026 Note
old_date = """                    if dt > datetime.datetime.now():
                        errors.append("Shipment date cannot be in the future")
                        quarantine_reasons.append("Shipment date cannot be in the future")
                except ValueError:"""
new_date = """                    if dt > datetime.datetime.now():
                        errors.append("Shipment date cannot be in the future")
                        quarantine_reasons.append("Shipment date cannot be in the future")
                    elif dt < datetime.datetime(2026, 1, 1):
                        notes.append("Pre-2026 shipment (reporting-only phase, no financial liability)")
                except ValueError:"""
code = code.replace(old_date, new_date)

# 2. Append `DeMinimis_Eligible_Mass_kg`
old_export = """            enriched_rows.append({
                **clean_row,
                "Matched_Material": matched_name,"""
new_export = """            
            is_deminimis_eligible = "NO"
            if sector_valid and sector_lower and not any(x in sector_lower for x in ['electric', 'hydrogen']):
                is_deminimis_eligible = "YES"
                
            enriched_rows.append({
                **clean_row,
                "DeMinimis_Eligible_Mass_kg": weight_kg if is_deminimis_eligible == "YES" else 0.0,
                "Matched_Material": matched_name,"""
code = code.replace(old_export, new_export)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Backend patched for de minimis logic and pre-2026.")
