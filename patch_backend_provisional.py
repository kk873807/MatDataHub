import os

def replace_between(text, start_str, end_str, replacement):
    start_idx = text.find(start_str)
    end_idx = text.find(end_str, start_idx) + len(end_str)
    return text[:start_idx] + replacement + text[end_idx:]

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the final dictionary construction block in `workflows.py`
old_dict = """            if quarantine_reasons:
                included_str = "NO: " + " | ".join(quarantine_reasons)
                total_co2_kg = 0.0
                total_co2_tonnes = 0.0
                cbam_cost_eur = 0.0
                esg_risk = 0.0
            else:
                included_str = "YES"

            clean_row = {}
            for k, v in row.to_dict().items():
                if isinstance(v, str) and str(v).startswith(('=', '+', '-', '@')):
                    clean_row[k] = f"'{v}"
                else:
                    clean_row[k] = v

            enriched_rows.append({
                **clean_row,
                "Matched_Material": matched_name,
                "Match_Confidence": f"{confidence}%" if is_match else "0%",
                "Carbon_Factor_kgCO2e_per_kg": round(carbon_factor, 3),
                "Emissions_Basis": emissions_basis,
                "Total_CO2_kg": round(total_co2_kg, 3) if total_co2_kg > 0 else 0.0,
                "Total_CO2_tonnes": round(total_co2_tonnes, 4) if total_co2_tonnes > 0 else 0.0,
                "Domestic_Carbon_Price_Paid_EUR": price_paid,
                "Net_CBAM_Price_EUR": net_cbam_price,
                "CBAM_Cost_EUR": cbam_cost_eur if cbam_cost_eur > 0 else 0.0,
                "Is_Obsolete": obsolete_flag,
                "Replacement_Standard": replacement,
                "ESG_Risk_Score": esg_risk if esg_risk > 0 else 0.0,
                "Notes": " | ".join(notes) if notes else "None",
                "Validation_Errors": " | ".join(errors) if errors else "None",
                "Included_In_Total": included_str
            })"""

new_dict = """            raw_total_co2_kg = total_co2_kg
            raw_total_co2_tonnes = total_co2_tonnes
            raw_cbam_cost_eur = cbam_cost_eur
            
            if quarantine_reasons:
                included_str = "NO: " + " | ".join(quarantine_reasons)
                total_co2_kg = 0.0
                total_co2_tonnes = 0.0
                cbam_cost_eur = 0.0
                esg_risk = 0.0
            else:
                included_str = "YES"

            clean_row = {}
            for k, v in row.to_dict().items():
                if isinstance(v, str) and str(v).startswith(('=', '+', '-', '@')):
                    clean_row[k] = f"'{v}"
                else:
                    clean_row[k] = v

            enriched_rows.append({
                **clean_row,
                "Matched_Material": matched_name,
                "Match_Confidence": f"{confidence}%" if is_match else "0%",
                "Carbon_Factor_kgCO2e_per_kg": round(carbon_factor, 3),
                "Emissions_Basis": emissions_basis,
                "Total_CO2_kg": round(total_co2_kg, 3) if total_co2_kg > 0 else 0.0,
                "Total_CO2_tonnes": round(total_co2_tonnes, 4) if total_co2_tonnes > 0 else 0.0,
                "CBAM_Cost_EUR": cbam_cost_eur if cbam_cost_eur > 0 else 0.0,
                "Provisional_CO2_kg": round(raw_total_co2_kg, 3),
                "Provisional_CO2_tonnes": round(raw_total_co2_tonnes, 4),
                "Provisional_CBAM_Cost_EUR": round(raw_cbam_cost_eur, 2),
                "Domestic_Carbon_Price_Paid_EUR": price_paid,
                "Net_CBAM_Price_EUR": net_cbam_price,
                "Is_Obsolete": obsolete_flag,
                "Replacement_Standard": replacement,
                "ESG_Risk_Score": esg_risk if esg_risk > 0 else 0.0,
                "Notes": " | ".join(notes) if notes else "None",
                "Validation_Errors": " | ".join(errors) if errors else "None",
                "Included_In_Total": included_str
            })"""

code = code.replace(old_dict, new_dict)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Added Provisional columns.")
