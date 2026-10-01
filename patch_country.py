import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix the greedy 'country' alias which matches 'destination_country'
old_country = """            # Country Validation (lightweight heuristic list)
            country = extract_string(['country', 'origin', 'supplier_country'])
            if not country:"""

new_country = """            # Country Validation (lightweight heuristic list)
            def extract_exact_string(aliases):
                for k in row.keys():
                    if any(a == str(k).lower().strip() for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                            return str(val).strip()
                return None
                
            country = extract_exact_string(['country_of_origin', 'supplier_country', 'origin', 'country'])
            if not country:"""

code = code.replace(old_country, new_country)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Country check fixed.")
