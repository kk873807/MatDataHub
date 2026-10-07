import pandas as pd
import time
import datetime

# Create dummy DF with 50k rows
df = pd.DataFrame([{f"col_{i}": f"val_{i}" for i in range(15)} for _ in range(50000)])

start = time.time()
for index, row in df.iterrows():
    def extract_string(aliases):
        for k in row.keys():
            k_lower = str(k).lower().strip()
            if any(a == k_lower for a in aliases):
                val = row[k]
                return str(val).strip()
        return None
    extract_string(['cn_code', 'hs_code'])
    extract_string(['country_of_origin', 'origin'])
    extract_string(['destination'])
    extract_string(['shipment_date'])
    extract_string(['cbam_sector'])
print(f"Elapsed: {time.time() - start:.2f}s")
