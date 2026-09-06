import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: tab_substitute radar chart keys
old_radar = "r=[base_mat.get('cost_per_kg', 0), base_mat.get('density', 0), base_mat.get('tensile_strength', 0), base_mat.get('embodied_carbon', 0)],"
new_radar = "r=[base_mat.get('cost_per_kg_min', 0), base_mat.get('density', 0), base_mat.get('tensile_strength_min', 0), base_mat.get('embodied_carbon', 0)],"
content = content.replace(old_radar, new_radar)

# Fix 2: tab_risk data key and currency conversion
# Locate the block in tab_risk
target_risk_old = """                                raw_cost = selected_mat.get("cost_per_kg")
                                
                                # DEEP DIVE FLAW FIX: Do not silently calculate zero if data is missing!
                                if raw_carbon is None or raw_cost is None or float(raw_carbon) == 0.0 or float(raw_cost) == 0.0:"""
target_risk_new = """                                raw_cost = selected_mat.get("cost_per_kg_min")
                                
                                # DEEP DIVE FLAW FIX: Do not silently calculate zero if data is missing!
                                if raw_carbon is None or raw_cost is None or float(raw_carbon) == 0.0 or float(raw_cost) == 0.0:"""
content = content.replace(target_risk_old, target_risk_new)

target_risk_math_old = """                                    # Financials (Unified to USD)
                                    annual_cbam_tax_usd = total_carbon_tons * cbam_price_usd
                                    material_cost_per_kg = float(raw_cost)
                                    annual_material_cost_usd = material_cost_per_kg * (volume_tons * 1000)"""
target_risk_math_new = """                                    # Financials (Unified to USD)
                                    annual_cbam_tax_usd = total_carbon_tons * cbam_price_usd
                                    material_cost_per_kg_inr = float(raw_cost)
                                    # Convert INR database values to USD (Assuming 1 INR = ~0.012 USD)
                                    material_cost_per_kg_usd = material_cost_per_kg_inr * 0.012
                                    annual_material_cost_usd = material_cost_per_kg_usd * (volume_tons * 1000)"""
content = content.replace(target_risk_math_old, target_risk_math_new)


# Fix 3: tab_enterprise keys and currency formatting
old_ent_math = """                                match = db_lookup.get(raw_name)
                                if match:
                                    carbon = float(match.get("embodied_carbon") or 0.0) * weight
                                    cost = float(match.get("cost_per_kg") or 0.0) * weight
                                    matched_count += 1
                                    total_carbon += carbon
                                    total_cost += cost
                                    
                                    results.append({
                                        "Original_Material": row[mat_col],
                                        "Weight_kg": weight,
                                        "Match_Status": "\u2705 Verified",
                                        "Matched_ID": match.get("id"),
                                        "Embodied_Carbon_kgCO2e": round(carbon, 2),
                                        "Est_Cost_USD": round(cost, 2)
                                    })
                                else:
                                    results.append({
                                        "Original_Material": row[mat_col],
                                        "Weight_kg": weight,
                                        "Match_Status": "\u274c Unmapped",
                                        "Matched_ID": None,
                                        "Embodied_Carbon_kgCO2e": 0.0,
                                        "Est_Cost_USD": 0.0
                                    })"""

new_ent_math = """                                match = db_lookup.get(raw_name)
                                if match:
                                    carbon = float(match.get("embodied_carbon") or 0.0) * weight
                                    cost_inr = float(match.get("cost_per_kg_min") or 0.0) * weight
                                    matched_count += 1
                                    total_carbon += carbon
                                    total_cost += cost_inr
                                    
                                    results.append({
                                        "Original_Material": row[mat_col],
                                        "Weight_kg": weight,
                                        "Match_Status": "\u2705 Verified",
                                        "Matched_ID": match.get("id"),
                                        "Embodied_Carbon_kgCO2e": round(carbon, 2),
                                        "Est_Cost_INR": round(cost_inr, 2)
                                    })
                                else:
                                    results.append({
                                        "Original_Material": row[mat_col],
                                        "Weight_kg": weight,
                                        "Match_Status": "\u274c Unmapped",
                                        "Matched_ID": None,
                                        "Embodied_Carbon_kgCO2e": 0.0,
                                        "Est_Cost_INR": 0.0
                                    })"""
content = content.replace(old_ent_math, new_ent_math)

old_ent_metric = 'm2.metric("Total Estimated Cost", f"${total_cost:,.2f}")'
new_ent_metric = 'm2.metric("Total Estimated Cost", f"\u20b9{total_cost:,.0f}")'
content = content.replace(old_ent_metric, new_ent_metric)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Keys and Currencies updated safely.")
