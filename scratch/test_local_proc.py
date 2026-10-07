import time
import pandas as pd
from app.database import SessionLocal
from app.workflows import BOMProcessor
import sys

print("Loading CSV...")
df = pd.read_csv("scripts/stress_test_50k.csv")
print(f"Loaded {len(df)} rows")

db = SessionLocal()
t0 = time.time()
print("Initializing BOMProcessor...")
proc = BOMProcessor(db)
print(f"Initialized in {time.time()-t0:.2f}s")

print("Processing BOM...")
t1 = time.time()
enriched_df = proc.process_bom(df, "Material", "Weight_kg")
print(f"Processed in {time.time()-t1:.2f}s")

print("Done!")
db.close()
