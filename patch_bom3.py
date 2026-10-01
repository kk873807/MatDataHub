import os
import re

file_path = 'app/workflows.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def replace_mat_col_logic():
    old = """        actual_mat_col = material_col
        if material_col not in df.columns:
            for guess in ["material", "name", "part", "component", "grade", "item", "description"]:
                matches = [c for c in df.columns if guess in str(c).lower()]
                if matches:
                    actual_mat_col = matches[0]
                    break"""
    
    new = """        actual_mat_col = material_col
        if material_col not in df.columns:
            # Prioritize 'name' or 'desc' columns, explicit exclude 'id'
            for guess in ["name", "material", "part", "component", "grade", "description", "item"]:
                matches = [c for c in df.columns if guess in str(c).lower() and "id" not in str(c).lower()]
                if matches:
                    actual_mat_col = matches[0]
                    break"""
    return content.replace(old, new)

content = replace_mat_col_logic()

def replace_inner_loop():
    old_marker = """            price_paid = extract_float(['carbon_price_paid', 'price_paid', 'domestic_carbon']) or 0.0"""
    new_insertion = """            price_paid = extract_float(['carbon_price_paid', 'price_paid', 'domestic_carbon']) or 0.0
            
            def extract_string(aliases):
                for k in row.keys():
                    if any(a in str(k).lower() for a in aliases):
                        return str(row[k]).strip()
                return None
                
            supplier_risk = extract_float(['supplier_risk', 'vendor_risk']) or 0.0
            single_source = extract_string(['single_source', 'sole_source'])
            geo_risk = extract_string(['geopolitical', 'geo_risk', 'country_risk'])"""
            
    content2 = content.replace(old_marker, new_insertion)
    
    old_esg = """            carbon_score = min(carbon_factor / 30.0 * 50, 50)
            recycle_score = (1 - recyclability) * 30
            obsolete_score = 20 if obsolete_flag == "YES" else 0
            esg_risk = round(min(carbon_score + recycle_score + obsolete_score, 100), 1)"""
            
    new_esg = """            carbon_score = min(carbon_factor / 30.0 * 50, 50)
            
            if geo_risk or single_source or supplier_risk > 0:
                geo_score = 15 if geo_risk and "high" in geo_risk.lower() else (7.5 if geo_risk and "med" in geo_risk.lower() else 0)
                ss_score = 15 if single_source and ("yes" in single_source.lower() or "true" in single_source.lower() or "y" == single_source.lower()) else 0
                supp_score = min(supplier_risk / 100.0 * 20, 20)
                base_esg = carbon_score + geo_score + ss_score + supp_score
            else:
                recycle_score = (1 - recyclability) * 30
                obsolete_score = 20 if obsolete_flag == "YES" else 0
                base_esg = carbon_score + recycle_score + obsolete_score
                
            esg_risk = round(min(base_esg, 100), 1)"""
            
    return content2.replace(old_esg, new_esg)

content = replace_inner_loop()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched workflows.py")
