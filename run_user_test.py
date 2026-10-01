import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from app.database import SessionLocal
from app.workflows import BOMProcessor

CSV_PATH = "user_edge_test.csv"

db = SessionLocal()
try:
    processor = BOMProcessor(db)
    df_in = pd.read_csv(CSV_PATH)
    print(f"Input: {len(df_in)} rows")
    
    df_out = processor.process_bom(df_in, "material_name", "quantity_tonnes")
    
    print(f"Output: {len(df_out)} rows")
    df_out.to_csv("user_edge_test_output.csv", index=False)
    
    for _, row in df_out.iterrows():
        print(f"{row.get('material_id', '?')}: {row.get('Validation_Errors', '')}")
finally:
    db.close()
