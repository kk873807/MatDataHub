import os
import re

file_path = 'app/workflows.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the inner loop of process_bom
def get_replacement():
    return """        enriched_rows = []
        for index, row in df.iterrows():
            raw_name = str(row.get(actual_mat_col, ""))
            raw_weight = row.get(actual_weight_col, 0.0)
            if pd.notna(raw_weight):
                try:
                    if isinstance(raw_weight, str):
                        raw_weight = raw_weight.replace(',', '')
                    weight_kg = float(raw_weight) * weight_multiplier
                except ValueError:
                    weight_kg = 0.0
            else:
                weight_kg = 0.0
                
            if not raw_name or str(raw_name).strip() == "" or str(raw_name).lower() == "nan":
                continue
                
            # Check for provided CBAM data in CSV
            def extract_float(aliases):
                for k in row.keys():
                    if any(a in str(k).lower() for a in aliases):
                        val = row[k]
                        if pd.notna(val):
                            try:
                                if isinstance(val, str): val = val.replace(',', '')
                                return float(val)
                            except ValueError:
                                pass
                return None

            direct_em = extract_float(['direct_emissions', 'direct emissions'])
            indirect_em = extract_float(['indirect_emissions', 'indirect emissions'])
            price_paid = extract_float(['carbon_price_paid', 'price_paid', 'domestic_carbon']) or 0.0
            
            provided_carbon_factor = None
            if direct_em is not None and indirect_em is not None:
                provided_carbon_factor = direct_em + indirect_em
            elif direct_em is not None:
                provided_carbon_factor = direct_em
                
            match_tuple = process.extractOne(raw_name, self.mat_names)
            # Increase threshold to 85 to prevent random bad matches (like Cement -> Steel)
            is_match = match_tuple and match_tuple[1] > 82
            
            if is_match:
                matched_name = match_tuple[0]
                confidence = match_tuple[1]
                mat = self.db.query(Material).filter(Material.name == matched_name).first()
                db_carbon = mat.embodied_carbon if mat.embodied_carbon else 0.0
                
                carbon_factor = provided_carbon_factor if provided_carbon_factor is not None else (db_carbon if db_carbon > 0 else _estimate_carbon_factor(mat.name, mat.category))
                obsolete_flag = "YES" if mat.is_obsolete else "NO"
                replacement = mat.replacement_standard if mat.replacement_standard else "N/A"
                recyclability = mat.recyclability_index if mat.recyclability_index else 0.5
            else:
                matched_name = "NO MATCH FOUND"
                confidence = 0
                carbon_factor = provided_carbon_factor if provided_carbon_factor is not None else _estimate_carbon_factor(raw_name, "")
                obsolete_flag = "N/A"
                replacement = "N/A"
                recyclability = 0.5
                
            total_co2_kg = round(weight_kg * carbon_factor, 3)
            total_co2_tonnes = total_co2_kg / 1000.0
            
            # Netting out domestic carbon price paid
            net_cbam_price = max(CBAM_REFERENCE_PRICE_EUR - price_paid, 0.0)
            cbam_cost_eur = round(total_co2_tonnes * net_cbam_price, 2)
            
            carbon_score = min(carbon_factor / 30.0 * 50, 50)
            recycle_score = (1 - recyclability) * 30
            obsolete_score = 20 if obsolete_flag == "YES" else 0
            esg_risk = round(min(carbon_score + recycle_score + obsolete_score, 100), 1)

            enriched_rows.append({
                **row.to_dict(),
                "Matched_Material": matched_name,
                "Match_Confidence": f"{confidence}%" if is_match else "0%",
                "Carbon_Factor_kgCO2e_per_kg": round(carbon_factor, 3),
                "Total_CO2_kg": round(total_co2_kg, 3),
                "Total_CO2_tonnes": round(total_co2_tonnes, 4),
                "Domestic_Carbon_Price_Paid_EUR": price_paid,
                "Net_CBAM_Price_EUR": net_cbam_price,
                "CBAM_Cost_EUR": cbam_cost_eur,
                "Is_Obsolete": obsolete_flag,
                "Replacement_Standard": replacement,
                "ESG_Risk_Score": esg_risk,
            })

        return pd.DataFrame(enriched_rows)"""

old_chunk = content[content.find("        enriched_rows = []"):content.find("return pd.DataFrame(enriched_rows)") + len("return pd.DataFrame(enriched_rows)")]

if old_chunk:
    content = content.replace(old_chunk, get_replacement())
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced logic in app/workflows.py")
else:
    print("Could not find the chunk")
