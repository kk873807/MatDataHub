"""Run the construction demo BOM through the engine and print provenance fields per row."""
import io
import pandas as pd
from app.database import SessionLocal
from app.workflows import BOMProcessor

CSV = """material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,release_date,supplier,importer
C1,Steel Rebar,120000,Iron & Steel,7214 20 00,China,Germany,2026-06-15,X,DE1
C2,Portland Cement,150000,Cement,2523 29 00,Turkey,Germany,2026-06-15,Y,DE1
C3,Aluminium Window Frames,40000,Aluminium,7610 10 00,China,Germany,2026-06-15,Z,DE1
C4,Float Glass,20000,,7005 29 25,China,Germany,2026-06-15,W,DE1
"""

db = SessionLocal()
p = BOMProcessor(db)
out = p.process_bom(pd.read_csv(io.StringIO(CSV)), "Material", "Weight_kg")
cols = ["Material", "Emissions_Basis", "Default_Match_Digits", "Default_Geography",
        "Default_Base_Value", "Default_Markup_Pct", "Carbon_Factor_kgCO2e_per_kg",
        "Total_CO2_tonnes", "CBAM_Cost_EUR", "Included_In_Total"]
pd.set_option("display.width", 250)
print(out[cols].to_string(index=False))
inc = out["Included_In_Total"].astype(str).str.startswith("YES")
print("\nSum CBAM_Cost_EUR (in scope):", round(out.loc[inc, "CBAM_Cost_EUR"].sum(), 2))
print("Sum Total_CO2_tonnes (in scope):", round(out.loc[inc, "Total_CO2_tonnes"].sum(), 3))
