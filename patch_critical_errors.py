import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace `errors = []` with `errors = []\n            critical_errors = []`
code = code.replace("            errors = []\n", "            errors = []\n            critical_errors = []\n")

# Upgrade specific appends to critical_errors
code = code.replace("errors.append(\"Duplicate material ID\")", "critical_errors.append(\"Duplicate material ID\")")
code = code.replace("errors.append(\"Negative quantity\")", "critical_errors.append(\"Negative quantity\")")
code = code.replace("errors.append(\"Quantity exceeds 100M kg limit\")", "critical_errors.append(\"Quantity exceeds 100M kg limit\")")
code = code.replace("errors.append(\"Sector not covered by CBAM\")", "critical_errors.append(\"Sector not covered by CBAM\")")

# For the missing quantity, it sets weight to 0 anyway so it naturally zeroes out, we don't need to force it.

# Fix the sector_valid logic:
old_sector_logic = """            else:
                sector_valid = False
                if cbam_sector: errors.append("Sector not covered by CBAM")"""
new_sector_logic = """            else:
                sector_valid = True # If missing, we assume valid and let fuzzy matcher decide
                if cbam_sector: 
                    critical_errors.append("Sector not covered by CBAM")
                    sector_valid = False"""
code = code.replace(old_sector_logic, new_sector_logic)

# Replace the zeroing condition
old_zero_logic = """            # If there are any validation errors, zero out the quantitative impacts
            # so they don't corrupt dashboard aggregations.
            if errors:"""
new_zero_logic = """            # If there are any validation errors, zero out the quantitative impacts
            # so they don't corrupt dashboard aggregations.
            if critical_errors:"""
code = code.replace(old_zero_logic, new_zero_logic)

# Replace the output column joining
old_output_logic = """                "Validation_Errors": " | ".join(errors) if errors else "None"
            })"""
new_output_logic = """                "Validation_Errors": " | ".join(critical_errors + errors) if (critical_errors or errors) else "None"
            })"""
code = code.replace(old_output_logic, new_output_logic)


with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Warnings vs Critical Errors logic applied.")
