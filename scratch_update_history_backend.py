import sys
import re

file_path = 'app/routers/materials.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the mocked history logic
old_history_logic = """
            now = datetime.utcnow()
            base_price = mat.cost_per_kg_min
            # Generate 12 months of fake historical volatility for demo
            history = []
            for i in range(12, 0, -1):
                past_date = now - timedelta(days=30*i)
                fluctuation = base_price * random.uniform(0.85, 1.15)
                history.append(
                    PriceHistoryResponse(
                        id=i, material_id=material_id, cost_per_kg=round(fluctuation, 2), recorded_date=past_date
                    )
                )
            # Add current price
            history.append(PriceHistoryResponse(id=0, material_id=material_id, cost_per_kg=base_price, recorded_date=now))
"""

new_history_logic = """
            now = datetime.utcnow()
            base_price = mat.cost_per_kg_min
            
            history = []
            
            # We want rolling 12 months ending in the PREVIOUS month.
            curr_month = now.month - 1
            curr_year = now.year
            if curr_month == 0:
                curr_month = 12
                curr_year -= 1
                
            for i in range(11, -1, -1):
                m = curr_month - i
                y = curr_year
                while m <= 0:
                    m += 12
                    y -= 1
                
                past_date = datetime(y, m, 1)
                fluctuation = base_price * random.uniform(0.85, 1.15)
                history.append(
                    PriceHistoryResponse(
                        id=i, material_id=material_id, cost_per_kg=round(fluctuation, 2), recorded_date=past_date
                    )
                )
"""

if "range(12, 0, -1):" in content:
    content = content.replace(old_history_logic, new_history_logic)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated backend to use strict calendar months.")
else:
    print("Could not find the history logic to replace.")
