import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# We'll use string replacement to inject validation logic.

# 1. Inject seen_ids and Error_Flags
code = code.replace(
    "enriched_rows = []\n        for index, row in df.iterrows():",
    "enriched_rows = []\n        seen_ids = set()\n        for index, row in df.iterrows():\n            errors = []"
)

# 2. Extract material_id and check duplicates
# Insert right after `errors = []`
code = code.replace(
    "            errors = []\n            raw_name = str(row.get(actual_mat_col, \"\"))",
    "            errors = []\n            \n            def extract_string(aliases):\n                for k in row.keys():\n                    if any(a in str(k).lower() for a in aliases):\n                        val = row[k]\n                        if pd.notna(val) and str(val).strip() != \"\" and str(val).lower() != \"nan\":\n                            return str(val).strip()\n                return None\n            \n            mat_id = extract_string(['material_id', 'id'])\n            if mat_id:\n                if mat_id in seen_ids:\n                    errors.append(\"Duplicate material ID\")\n                else:\n                    seen_ids.add(mat_id)\n\n            raw_name = str(row.get(actual_mat_col, \"\"))"
)
# Note: we need to remove the later definition of `extract_string` to avoid redefinition/scope issues.
code = code.replace(
    "            def extract_string(aliases):\n                for k in row.keys():\n                    if any(a in str(k).lower() for a in aliases):\n                        return str(row[k]).strip()\n                return None\n                \n            supplier_risk",
    "            supplier_risk"
)

# 3. Handle raw_weight validations
old_weight_logic = """            raw_weight = row.get(actual_weight_col, 0.0)
            if pd.notna(raw_weight):
                try:
                    if isinstance(raw_weight, str):
                        raw_weight = raw_weight.replace(',', '')
                    weight_kg = float(raw_weight) * weight_multiplier
                    if weight_kg < 0:
                        weight_kg = 0.0
                except ValueError:
                    weight_kg = 0.0
            else:
                weight_kg = 0.0"""

new_weight_logic = """            raw_weight = row.get(actual_weight_col, None)
            if pd.isna(raw_weight) or str(raw_weight).strip() == "" or str(raw_weight).lower() == "nan":
                errors.append("Missing quantity")
                weight_kg = 0.0
            else:
                try:
                    if isinstance(raw_weight, str):
                        raw_weight = str(raw_weight).replace(',', '')
                    weight_kg = float(raw_weight) * weight_multiplier
                    if weight_kg < 0:
                        errors.append("Negative quantity")
                        weight_kg = 0.0
                    elif weight_kg > 100_000_000:
                        errors.append("Quantity exceeds 100M kg limit")
                except ValueError:
                    errors.append("Non-numeric quantity")
                    weight_kg = 0.0"""
code = code.replace(old_weight_logic, new_weight_logic)

# 4. Handle raw_name
old_name_logic = """            if not raw_name or str(raw_name).strip() == "" or str(raw_name).lower() == "nan":
                continue"""
new_name_logic = """            if not raw_name or str(raw_name).strip() == "" or str(raw_name).lower() == "nan":
                errors.append("Missing material name")
                raw_name = "UNKNOWN" """
code = code.replace(old_name_logic, new_name_logic)

# 5. Handle float fields (emissions, price, risk)
old_extract_float = """            # Check for provided CBAM data in CSV
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
                return None"""
new_extract_float = """            # Check for provided CBAM data in CSV
            def extract_float(aliases, field_name):
                for k in row.keys():
                    if any(a in str(k).lower() for a in aliases):
                        val = row[k]
                        if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                            # We found the column, but it's empty
                            if field_name: errors.append(f"Missing {field_name}")
                            return None
                        try:
                            if isinstance(val, str): val = val.replace(',', '')
                            return float(val)
                        except ValueError:
                            if field_name: errors.append(f"Non-numeric {field_name}")
                            return None
                return None"""
code = code.replace(old_extract_float, new_extract_float)

code = code.replace("direct_em = extract_float(['direct_emissions', 'direct emissions'])", "direct_em = extract_float(['direct_emissions', 'direct emissions'], 'direct emissions')")
code = code.replace("indirect_em = extract_float(['indirect_emissions', 'indirect emissions'])", "indirect_em = extract_float(['indirect_emissions', 'indirect emissions'], 'indirect emissions')")
code = code.replace("price_paid = extract_float(['carbon_price_paid', 'price_paid', 'domestic_carbon']) or 0.0", "price_paid_val = extract_float(['carbon_price_paid', 'price_paid', 'domestic_carbon'], None)\n            price_paid = price_paid_val or 0.0")
code = code.replace("supplier_risk = extract_float(['supplier_risk', 'vendor_risk']) or 0.0", "supplier_risk = extract_float(['supplier_risk', 'vendor_risk'], 'supplier risk') or 0.0")

# 6. Valid enums
code = code.replace(
    "            single_source = extract_string(['single_source', 'sole_source'])\n            geo_risk = extract_string(['geopolitical', 'geo_risk', 'country_risk'])",
    "            single_source = extract_string(['single_source', 'sole_source'])\n            if single_source and single_source.lower() not in ('yes', 'no', 'true', 'false', 'y', 'n'):\n                errors.append(\"Invalid single_source_flag\")\n            geo_risk = extract_string(['geopolitical', 'geo_risk', 'country_risk'])\n            if geo_risk and geo_risk.lower() not in ('low', 'medium', 'high'):\n                errors.append(\"Invalid geopolitical_risk\")\n            data_quality = extract_string(['data_quality', 'data quality'])\n            if data_quality and data_quality.lower() == 'verified' and price_paid_val is None:\n                errors.append(\"Missing carbon price for Verified data\")"
)

# 7. Sector validation
old_sector_logic = """            cbam_sector = extract_string(['cbam_sector', 'sector'])
            candidates = self.mat_names  # default: all names (already length-filtered)

            if cbam_sector and cbam_sector.lower() not in ('nan', ''):
                # Pre-filter candidates to the relevant DB category
                sector_lower = cbam_sector.strip().lower()
                allowed_cats = None  # None = sector not in map, keep all candidates
                for keyword, cats in self.CBAM_SECTOR_CATEGORY_MAP.items():
                    if keyword in sector_lower:
                        allowed_cats = cats  # [] = known sector, no DB category
                        break"""

new_sector_logic = """            cbam_sector = extract_string(['cbam_sector', 'sector'])
            candidates = self.mat_names  # default: all names (already length-filtered)

            sector_valid = True
            if cbam_sector and cbam_sector.lower() not in ('nan', ''):
                sector_lower = cbam_sector.strip().lower()
                allowed_cats = None
                for keyword, cats in self.CBAM_SECTOR_CATEGORY_MAP.items():
                    if keyword in sector_lower:
                        allowed_cats = cats
                        break
                
                if allowed_cats is None:
                    # Unrecognized sector like Textiles or Automotive
                    errors.append("Sector not covered by CBAM")
                    sector_valid = False
                elif allowed_cats:
                    # Known CBAM sector, filter to categories"""
code = code.replace(old_sector_logic, new_sector_logic)

# Replace the inner branch logic
code = code.replace(
    """                if allowed_cats is not None:  # sector was recognized
                    if allowed_cats:
                        # Merge candidates from matching DB categories
                        candidates = []
                        for cat in allowed_cats:
                            candidates.extend(self.cat_to_names.get(cat, []))
                        if not candidates:
                            candidates = []  # no DB entries for this category
                    else:
                        # Known CBAM sector with no DB counterpart (Fertilisers,
                        # Hydrogen) — skip matching entirely, force NO MATCH
                        candidates = []""",
    """                    candidates = []
                    for cat in allowed_cats:
                        candidates.extend(self.cat_to_names.get(cat, []))
                    if not candidates:
                        candidates = []
                elif allowed_cats == []:
                    # Fertilisers, Hydrogen
                    candidates = []
            else:
                sector_valid = False
                if cbam_sector: errors.append("Sector not covered by CBAM")"""
)

# 8. Set CBAM cost to 0 if invalid sector
code = code.replace(
    "            # Netting out domestic carbon price paid\n            net_cbam_price = max(CBAM_REFERENCE_PRICE_EUR - price_paid, 0.0)\n            cbam_cost_eur = round(total_co2_tonnes * net_cbam_price, 2)",
    "            # Netting out domestic carbon price paid\n            net_cbam_price = max(CBAM_REFERENCE_PRICE_EUR - price_paid, 0.0)\n            cbam_cost_eur = round(total_co2_tonnes * net_cbam_price, 2) if sector_valid else 0.0"
)

# 9. Output Validation_Errors column
code = code.replace(
    "                \"ESG_Risk_Score\": esg_risk,\n            })",
    "                \"ESG_Risk_Score\": esg_risk,\n                \"Validation_Errors\": \" | \".join(errors) if errors else \"None\"\n            })"
)


with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("workflows.py updated successfully.")
