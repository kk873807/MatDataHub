import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# Add Date Validation
old_logic = """                if len(c_lower) < 2 or c_lower in invalid_countries:
                    errors.append("Unrecognized country")
            
            provided_carbon_factor = None"""

new_logic = """                if len(c_lower) < 2 or c_lower in invalid_countries:
                    errors.append("Unrecognized country")
                    
            # Date validation
            shipment_date = extract_string(['last_shipment_date', 'shipment_date', 'date'])
            if shipment_date:
                import datetime
                try:
                    dt = datetime.datetime.strptime(shipment_date, "%Y-%m-%d")
                    if dt > datetime.datetime.now():
                        errors.append("Shipment date cannot be in the future")
                except ValueError:
                    errors.append("Invalid date format (requires YYYY-MM-DD)")
            
            provided_carbon_factor = None"""

code = code.replace(old_logic, new_logic)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Date validation applied.")
