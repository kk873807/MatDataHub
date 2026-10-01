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

# 1. Update extract_string and Material ID extraction
old_extract = """            def extract_string(aliases):
                for k in row.keys():
                    if any(a in str(k).lower() for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                            return str(val).strip()
                return None
            
            mat_id = extract_string(['material_id', 'id', 'item'])
            if not mat_id:
                errors.append("Missing material ID")
                quarantine_reasons.append("Missing material ID")
            else:
                mat_id_lower = str(mat_id).strip().lower()
                if mat_id_lower in seen_ids:
                    quarantine_reasons.append("Duplicate material ID")
                else:
                    seen_ids.add(mat_id_lower)"""

new_extract = """            def extract_string(aliases):
                for k in row.keys():
                    k_lower = str(k).lower().strip()
                    # Prevent 'id' from matching 'width', 'solid', 'liquid'
                    if any(a == k_lower or k_lower.startswith(a + '_') or k_lower.endswith('_' + a) for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                            return str(val).strip()
                return None
            
            mat_id = extract_string(['material_id', 'id', 'item_no', 'part_number'])
            if not mat_id:
                errors.append("Missing material ID")
                quarantine_reasons.append("Missing material ID")
            else:
                mat_id_lower = str(mat_id).strip().lower()
                if mat_id_lower in seen_ids:
                    quarantine_reasons.append("Duplicate material ID")
                else:
                    seen_ids.add(mat_id_lower)"""

code = code.replace(old_extract, new_extract)

# 2. Fix Missing Material Name quarantine and Missing Date quarantine
old_name_date = """            if not raw_name or str(raw_name).strip() == "" or str(raw_name).lower() == "nan":
                errors.append("Missing material name")
                quarantine_reasons.append("Missing material name")
                raw_name = "UNKNOWN" """

new_name_date = """            if not raw_name or str(raw_name).strip() == "" or str(raw_name).lower() == "nan":
                errors.append("Missing material name")
                raw_name = "UNKNOWN" """

code = code.replace(old_name_date, new_name_date)

old_date_logic = """            shipment_date = extract_string(['last_shipment_date', 'shipment_date', 'date'])
            if shipment_date:
                import datetime
                try:
                    dt = datetime.datetime.strptime(shipment_date, "%Y-%m-%d")
                    if dt > datetime.datetime.now():
                        errors.append("Shipment date cannot be in the future")
                        quarantine_reasons.append("Shipment date cannot be in the future")
                except ValueError:
                    errors.append("Invalid date format (requires YYYY-MM-DD)")
                    quarantine_reasons.append("Invalid date format")"""

new_date_logic = """            shipment_date = extract_string(['last_shipment_date', 'shipment_date', 'date'])
            if not shipment_date:
                errors.append("Missing shipment date")
                quarantine_reasons.append("Missing shipment date")
            else:
                import datetime
                try:
                    dt = datetime.datetime.strptime(shipment_date, "%Y-%m-%d")
                    if dt > datetime.datetime.now():
                        errors.append("Shipment date cannot be in the future")
                        quarantine_reasons.append("Shipment date cannot be in the future")
                except ValueError:
                    errors.append("Invalid date format (requires YYYY-MM-DD)")
                    quarantine_reasons.append("Invalid date format")"""

code = code.replace(old_date_logic, new_date_logic)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Backend patched for ID logic, Missing Name logic, and Date logic.")
