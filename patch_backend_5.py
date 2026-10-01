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

old_export = """            enriched_rows.append({
                **clean_row,
                "DeMinimis_Eligible_Mass_kg": weight_kg if is_deminimis_eligible == "YES" else 0.0,
                "Matched_Material": matched_name,"""
new_export = """            enriched_rows.append({
                **clean_row,
                "Parsed_Weight_kg": round(weight_kg, 2),
                "DeMinimis_Eligible_Mass_kg": weight_kg if is_deminimis_eligible == "YES" else 0.0,
                "Matched_Material": matched_name,"""
code = code.replace(old_export, new_export)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)
