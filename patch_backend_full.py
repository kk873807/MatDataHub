import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# I will replace the inside of `for index, row in df.iterrows():` loop.
# Let's extract the part that needs replacing.

def replace_between(text, start_str, end_str, replacement):
    start_idx = text.find(start_str)
    end_idx = text.find(end_str, start_idx) + len(end_str)
    return text[:start_idx] + replacement + text[end_idx:]

new_loop = """        for index, row in df.iterrows():
            errors = []
            quarantine_reasons = []
            
            def extract_string(aliases):
                for k in row.keys():
                    if any(a in str(k).lower() for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                            return str(val).strip()
                return None
            
            mat_id = extract_string(['material_id', 'id'])
            if not mat_id:
                errors.append("Missing material ID")
                quarantine_reasons.append("Missing material ID")
            else:
                mat_id_lower = str(mat_id).strip().lower()
                if mat_id_lower in seen_ids:
                    quarantine_reasons.append("Duplicate material ID")
                else:
                    seen_ids.add(mat_id_lower)

            raw_name = str(row.get(actual_mat_col, ""))
            raw_weight = row.get(actual_weight_col, None)
            if pd.isna(raw_weight) or str(raw_weight).strip() == "" or str(raw_weight).lower() == "nan":
                errors.append("Missing quantity")
                quarantine_reasons.append("Missing quantity")
                weight_kg = 0.0
            else:
                try:
                    if isinstance(raw_weight, str):
                        raw_weight = str(raw_weight).replace(',', '')
                    weight_kg = float(raw_weight) * weight_multiplier
                    if weight_kg < 0:
                        quarantine_reasons.append("Negative quantity")
                        weight_kg = 0.0
                    elif weight_kg > 100_000_000:
                        quarantine_reasons.append("Quantity exceeds 100M kg limit")
                except ValueError:
                    errors.append("Non-numeric quantity")
                    quarantine_reasons.append("Non-numeric quantity")
                    weight_kg = 0.0
                
            if not raw_name or str(raw_name).strip() == "" or str(raw_name).lower() == "nan":
                errors.append("Missing material name")
                quarantine_reasons.append("Missing material name")
                raw_name = "UNKNOWN" 
                
            # Check for provided CBAM data in CSV
            def extract_float(aliases, field_name):
                for k in row.keys():
                    if any(a in str(k).lower() for a in aliases):
                        val = row[k]
                        if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                            if field_name: errors.append(f"Missing {field_name}")
                            return None
                        try:
                            if isinstance(val, str):
                                val = str(val).replace('€', '').replace('$', '').strip()
                                if ',' in val and '.' not in val:
                                    parts = val.split(',')
                                    if len(parts[-1]) == 3:
                                        val = val.replace(',', '')
                                    else:
                                        val = val.replace(',', '.')
                                elif ',' in val and '.' in val:
                                    val = val.replace(',', '')
                            return float(val)
                        except ValueError:
                            if field_name: errors.append(f"Non-numeric {field_name}")
                            return None
                return None

            direct_em = extract_float(['direct_emissions', 'direct emissions'], 'direct emissions')
            indirect_em = extract_float(['indirect_emissions', 'indirect emissions'], 'indirect emissions')
            
            if direct_em is not None and direct_em > 50.0:
                quarantine_reasons.append("Emissions exceed plausibility bound (50 t/t)")
            if indirect_em is not None and indirect_em > 50.0:
                quarantine_reasons.append("Emissions exceed plausibility bound (50 t/t)")
                
            price_paid_val = extract_float(['carbon_price_paid', 'price_paid', 'domestic_carbon'], None)
            price_paid = price_paid_val or 0.0
            if price_paid < 0:
                errors.append("Carbon price cannot be negative")
                price_paid = 0.0
            
            supplier_risk = extract_float(['supplier_risk', 'vendor_risk'], 'supplier risk') or 0.0
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
                errors.append("Missing carbon price for Verified data")
                
            # CN Code Validation
            cn_code = extract_string(['cn_code', 'hs_code', 'cn code'])
            clean_cn = ""
            if cn_code:
                clean_cn = cn_code.replace(" ", "").replace(".", "").replace("-", "")
                if not clean_cn.isdigit() or len(clean_cn) < 4:
                    errors.append("Invalid CN Code format")
                
            # Country Validation
            def extract_exact_string(aliases):
                for k in row.keys():
                    if any(a == str(k).lower().strip() for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                            return str(val).strip()
                return None

            def clean_country(c):
                c = c.lower().strip()
                if c == 'the netherlands': return 'netherlands'
                if c == 'usa' or c == 'united states of america': return 'united states'
                if c == 'uk' or c == 'great britain': return 'united kingdom'
                return c
                
            country = extract_exact_string(['country_of_origin', 'supplier_country', 'origin', 'country'])
            if not country:
                errors.append("Missing supplier country")
                quarantine_reasons.append("Missing origin country")
            else:
                c_lower = clean_country(country)
                invalid_countries = ['nowhereland', 'atlantis', 'narnia', 'test', 'unknown']
                if len(c_lower) < 2 or c_lower in invalid_countries:
                    errors.append("Unrecognized country")
                    quarantine_reasons.append("Unrecognized origin country")
                if c_lower in self.EU_EEA_COUNTRIES:
                    errors.append("Origin is exempt from CBAM (EU/EEA)")
                    
            destination = extract_exact_string(['destination', 'destination_country'])
            if not destination:
                errors.append("Missing destination country")
                quarantine_reasons.append("Missing destination country")
            else:
                d_lower = clean_country(destination)
                invalid_countries = ['nowhereland', 'atlantis', 'narnia', 'test', 'unknown']
                if len(d_lower) < 2 or d_lower in invalid_countries:
                    errors.append("Unrecognized destination country")
                    quarantine_reasons.append("Unrecognized destination country")
                elif d_lower not in self.EU_EEA_COUNTRIES:
                    errors.append("Destination outside EU (exempt)")
                    
            # Date validation
            shipment_date = extract_string(['last_shipment_date', 'shipment_date', 'date'])
            if shipment_date:
                import datetime
                try:
                    dt = datetime.datetime.strptime(shipment_date, "%Y-%m-%d")
                    if dt > datetime.datetime.now():
                        errors.append("Shipment date cannot be in the future")
                        quarantine_reasons.append("Shipment date cannot be in the future")
                except ValueError:
                    errors.append("Invalid date format (requires YYYY-MM-DD)")
                    quarantine_reasons.append("Invalid date format")
            
            # --- Sector-aware fuzzy matching ---
            cbam_sector = extract_string(['cbam_sector', 'sector'])
            candidates = self.mat_names  # default: all names (already length-filtered)

            sector_valid = True
            sector_lower = ""
            allowed_cats = None
            if cbam_sector and cbam_sector.lower() not in ('nan', ''):
                sector_lower = cbam_sector.strip().lower()
                for keyword, cats in self.CBAM_SECTOR_CATEGORY_MAP.items():
                    if keyword in sector_lower:
                        allowed_cats = cats
                        break
                
                if allowed_cats is None:
                    quarantine_reasons.append("Sector not covered by CBAM")
                    errors.append("Sector not covered by CBAM")
                    sector_valid = False
                elif allowed_cats:
                    candidates = []
                    for cat in allowed_cats:
                        candidates.extend(self.cat_to_names.get(cat, []))
                    if not candidates:
                        candidates = []
                elif allowed_cats == []:
                    candidates = []
            else:
                sector_valid = True
                if cbam_sector: 
                    quarantine_reasons.append("Sector not covered by CBAM")
                    errors.append("Sector not covered by CBAM")
                    sector_valid = False

            match_tuple = process.extractOne(
                raw_name, candidates, scorer=fuzz.token_sort_ratio
            ) if candidates else None
            is_match = match_tuple and match_tuple[1] > 60

            provided_carbon_factor = None
            includes_indirect = False
            if allowed_cats is not None:
                if any(k in sector_lower for k in ['cement', 'fertili']):
                    includes_indirect = True
            
            if direct_em is not None:
                provided_carbon_factor = direct_em
                if includes_indirect and indirect_em is not None:
                    provided_carbon_factor += indirect_em
                elif not includes_indirect and indirect_em is not None:
                    errors.append("Note: Indirect emissions excluded for this sector (CBAM definitive rules)")

            if clean_cn and sector_lower:
                if "steel" in sector_lower or "iron" in sector_lower:
                    if not clean_cn.startswith(("72", "73", "26")):
                        errors.append("CN Code does not match Iron & Steel sector")
                        quarantine_reasons.append("CN Code does not match Iron & Steel sector")
                elif "cement" in sector_lower:
                    if not clean_cn.startswith("2523"):
                        errors.append("CN Code does not match Cement sector")
                        quarantine_reasons.append("CN Code does not match Cement sector")
                elif "alumin" in sector_lower:
                    if not clean_cn.startswith("76"):
                        errors.append("CN Code does not match Aluminium sector")
                        quarantine_reasons.append("CN Code does not match Aluminium sector")
                elif "fertil" in sector_lower:
                    if not clean_cn.startswith(("2808", "2814", "2834", "3102", "3105")):
                        errors.append("CN Code does not match Fertilisers sector")
                        quarantine_reasons.append("CN Code does not match Fertilisers sector")

            if is_match:
                q_lower = raw_name.lower()
                m_lower = match_tuple[0].lower()
                q_is_stainless = "stainless" in q_lower
                m_is_stainless = "stainless" in m_lower
                if q_is_stainless != m_is_stainless and "steel" in q_lower:
                    is_match = False
            
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
            
            net_cbam_price = max(CBAM_REFERENCE_PRICE_EUR - price_paid, 0.0)
            
            # Exemptions force cost to 0
            is_exempt = False
            if "Origin is exempt from CBAM (EU/EEA)" in errors:
                is_exempt = True
            if "Destination outside EU (exempt)" in errors:
                is_exempt = True
            
            cbam_cost_eur = round(total_co2_tonnes * net_cbam_price, 2) if sector_valid and not is_exempt else 0.0
            
            carbon_score = min(carbon_factor / 30.0 * 50, 50)
            if geo_risk or single_source or supplier_risk > 0:
                geo_score = 15 if geo_risk and "high" in geo_risk.lower() else (7.5 if geo_risk and "med" in geo_risk.lower() else 0)
                ss_score = 15 if single_source and ("yes" in single_source.lower() or "true" in single_source.lower() or "y" == single_source.lower()) else 0
                supp_score = min(supplier_risk / 100.0 * 20, 20)
                base_esg = carbon_score + geo_score + ss_score + supp_score
            else:
                recycle_score = (1 - recyclability) * 30
                obsolete_score = 20 if obsolete_flag == "YES" else 0
                base_esg = carbon_score + recycle_score + obsolete_score
            esg_risk = round(min(base_esg, 100), 1)

            # Do not ZERO the mathematical values out if they just have validation reasons!
            # The dashboard handles exclusion via Included_In_Total.
            if quarantine_reasons:
                included_str = "NO: " + " | ".join(quarantine_reasons)
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
                "Total_CO2_kg": round(total_co2_kg, 3),
                "Total_CO2_tonnes": round(total_co2_tonnes, 4),
                "Domestic_Carbon_Price_Paid_EUR": price_paid,
                "Net_CBAM_Price_EUR": net_cbam_price,
                "CBAM_Cost_EUR": cbam_cost_eur,
                "Is_Obsolete": obsolete_flag,
                "Replacement_Standard": replacement,
                "ESG_Risk_Score": esg_risk,
                "Validation_Errors": " | ".join(errors) if errors else "None",
                "Included_In_Total": included_str
            })

        return pd.DataFrame(enriched_rows)"""

start_str = "        for index, row in df.iterrows():"
end_str = "        return pd.DataFrame(enriched_rows)"

code = replace_between(code, start_str, end_str, new_loop)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Replaced process_bom perfectly.")
