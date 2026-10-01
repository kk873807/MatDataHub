import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# We want to intercept total_co2_kg and cbam_cost_eur right before they are appended to enriched_rows.
old_tail = """            esg_risk = round(min(base_esg, 100), 1)

            enriched_rows.append({"""

new_tail = """            esg_risk = round(min(base_esg, 100), 1)

            # If there are any validation errors, zero out the quantitative impacts
            # so they don't corrupt dashboard aggregations.
            if errors:
                total_co2_kg = 0.0
                total_co2_tonnes = 0.0
                cbam_cost_eur = 0.0
                esg_risk = 0.0

            enriched_rows.append({"""

code = code.replace(old_tail, new_tail)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Zeroing logic added successfully.")
