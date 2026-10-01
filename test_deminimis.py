import pandas as pd
from app.workflows import BOMProcessor

df = pd.DataFrame([
    {"material_id": "TH-A1", "material_name": "Steel", "weight_kg": 40200, "cbam_sector": "Iron & Steel", "direct_emissions": 2.0, "indirect_emissions": 0.0, "carbon_price_paid": 0, "supplier_name": "S1", "country_of_origin": "China", "destination_country": "Germany", "shipment_date": "2026-06-01"},
    {"material_id": "TH-A2", "material_name": "Cement", "weight_kg": 13050, "cbam_sector": "Cement", "direct_emissions": 0.8, "indirect_emissions": 0.2, "carbon_price_paid": 0, "supplier_name": "S1", "country_of_origin": "China", "destination_country": "Germany", "shipment_date": "2026-06-01"},
    {"material_id": "TH-A3", "material_name": "Hydrogen", "weight_kg": 95000, "cbam_sector": "Hydrogen", "direct_emissions": 10.0, "indirect_emissions": 0.0, "carbon_price_paid": 0, "supplier_name": "S1", "country_of_origin": "China", "destination_country": "Germany", "shipment_date": "2026-06-01"}
])

# For Steel, eligible = 40200.
# For Cement, eligible = 13050.
# For Hydrogen, eligible = 0.
# Total eligible = 53250. Wait! The user said: "40.2 + 13.05 + 27.26 = 80.51 t".
# Let's adjust weights so eligible <= 50,000.
df.loc[1, "weight_kg"] = 9000  # Cement 9t. Total = 49.2t.

class DummyDB:
    def query(self, *args, **kwargs):
        class DummyQ:
            def filter(self, *a, **k): return self
            def first(self):
                class Mat:
                    embodied_carbon = 0.0
                    is_obsolete = False
                    replacement_standard = None
                    recyclability_index = 0.5
                    name = "Steel"
                    category = "metal"
                return Mat()
        return DummyQ()

processor = BOMProcessor(db=DummyDB())
enriched = processor.process_bom(df, "material_name", "weight_kg")

for _, r in enriched.iterrows():
    print(f"{r['material_id']} | Eligible Mass: {r.get('DeMinimis_Eligible_Mass_kg')} | Tax: {r['CBAM_Cost_EUR']} | Notes: {r['Notes']}")
