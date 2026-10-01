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

old_return = """        return pd.DataFrame(enriched_rows)"""
new_return = """        total_eligible_mass_kg = sum(r.get("DeMinimis_Eligible_Mass_kg", 0.0) for r in enriched_rows if r.get("Included_In_Total", "").startswith("YES"))
        
        if 0 < total_eligible_mass_kg <= 50000.0:
            for r in enriched_rows:
                if r.get("Included_In_Total", "").startswith("YES") and r.get("DeMinimis_Eligible_Mass_kg", 0.0) > 0:
                    r["Provisional_CBAM_Cost_EUR"] = r["CBAM_Cost_EUR"]
                    r["CBAM_Cost_EUR"] = 0.0
                    current_notes = r.get("Notes", "None")
                    new_note = "De minimis exemption applies (annual eligible total <= 50t)"
                    if current_notes == "None":
                        r["Notes"] = new_note
                    else:
                        r["Notes"] = current_notes + " | " + new_note

        return pd.DataFrame(enriched_rows)"""
code = code.replace(old_return, new_return)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Backend patched successfully.")
