import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from app.database import SessionLocal
from app.workflows import BOMProcessor
import traceback

def run_test():
    db = SessionLocal()
    try:
        processor = BOMProcessor(db)
        
        # Let's create a nasty dataframe
        data = {
            "material_name": ["Steel", "Cement", "Unknown", None, "nan", ""],
            "weight_kg": [1000, "1000", -500, None, "five hundred", 1000000000],
            "cbam_sector": ["Iron & Steel", "Cement", "Automotive", "Electricity", None, "nan"],
            "country_of_origin": ["China", "Nowhereland", None, "Atlantis", "US", "DE"],
            "last_shipment_date": ["2026-08-14", "14/08/2026", "2030-01-01", None, "nan", "2023-01-01"],
            "cn_code": ["7208", "ABCD-XYZ", "72.08", "72085100", None, "123"],
            "supplier_risk": [10, "Very High", None, 150, 0, "50"],
            "single_source": ["Yes", "Maybe", None, "True", "N", "False"],
            "direct_emissions": [1.5, "unknown", None, 999.99, 0.0, 1.0],
            "indirect_emissions": [0.5, 0.1, None, 0.0, 0.0, "N/A"],
            "carbon_price_paid": [0, 100, None, 75, "74.99", "50 EUR"],
            "data_quality": ["Verified", "Estimated", None, "Verified", "Default", "Verified"]
        }
        df = pd.DataFrame(data)
        
        print("Running processor...")
        df_out = processor.process_bom(df, "material_name", "weight_kg")
        print("Success! Output rows:", len(df_out))
        print(df_out[['material_name', 'Validation_Errors']].to_string())
        
    except Exception as e:
        print("CRASHED!")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    run_test()
