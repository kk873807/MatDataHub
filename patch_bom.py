import os

file_path = 'app/workflows.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """    def process_bom(self, df, material_col, weight_col):
        enriched_rows = []
        for index, row in df.iterrows():
            raw_name = str(row.get(material_col, ""))
            raw_weight = row.get(weight_col, 0.0)
            if pd.notna(raw_weight):
                try:
                    if isinstance(raw_weight, str):
                        raw_weight = raw_weight.replace(',', '')
                    weight_kg = float(raw_weight)
                except ValueError:
                    weight_kg = 0.0
            else:
                weight_kg = 0.0
            if not raw_name:
                continue"""

new_logic = """    def process_bom(self, df, material_col, weight_col):
        # Auto-detect column mappings if the explicit ones are missing
        actual_mat_col = material_col
        if material_col not in df.columns:
            for guess in ["material", "name", "part", "component", "grade", "item", "description"]:
                matches = [c for c in df.columns if guess in str(c).lower()]
                if matches:
                    actual_mat_col = matches[0]
                    break
                    
        actual_weight_col = weight_col
        if weight_col not in df.columns:
            for guess in ["weight", "qty", "quantity", "mass", "amount"]:
                matches = [c for c in df.columns if guess in str(c).lower()]
                if matches:
                    actual_weight_col = matches[0]
                    break
        
        # Determine multiplier if weight is in tonnes
        weight_multiplier = 1.0
        if actual_weight_col in df.columns and ("tonne" in str(actual_weight_col).lower() or "ton" in str(actual_weight_col).lower()):
            weight_multiplier = 1000.0

        enriched_rows = []
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
                continue"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Could not find exact block to replace")
