"""
Seed the cbam_defaults table with EU Commission definitive-period default values.

Sources:
- EC Implementing Regulation 2023/1773 (transitional base values)
- EC Regulation 2023/956 Art. 7 (definitive-period markup schedule)
- Definitive period: +10% (2026), +20% (2027), +30% (2028+)

Run:
    python scripts/seed_cbam_defaults.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, Base
from app.models import CBAMDefault

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------
# Transitional-period base values (tCO2 per tonne of product)
# These are the starting point; the definitive-period markup is applied on top.
# -------------------------------------------------------------------
BASE_DEFAULTS = [
    # Iron & Steel products (direct emissions only)
    ("72",   "Iron & Steel", "Pig iron / spiegeleisen",           2.09, False),
    ("7201", "Iron & Steel", "Pig iron",                          2.09, False),
    ("7202", "Iron & Steel", "Ferro-alloys",                      2.09, False),
    ("7203", "Iron & Steel", "Ferrous products (direct-reduced)", 1.60, False),
    ("7205", "Iron & Steel", "Granules and powders",              2.01, False),
    ("7206", "Iron & Steel", "Iron ingots",                       2.01, False),
    ("7207", "Iron & Steel", "Semi-finished products of iron",    2.01, False),
    ("7208", "Iron & Steel", "Hot-rolled flat products",          2.01, False),
    ("7209", "Iron & Steel", "Cold-rolled flat products",         2.12, False),
    ("7210", "Iron & Steel", "Coated flat products",              2.22, False),
    ("7211", "Iron & Steel", "Flat-rolled products (other)",      2.01, False),
    ("7213", "Iron & Steel", "Hot-rolled bars and rods",          2.01, False),
    ("7214", "Iron & Steel", "Bars and rods (forged/cold-formed)",2.01, False),
    ("7215", "Iron & Steel", "Other bars and rods",               2.01, False),
    ("7216", "Iron & Steel", "Angles, shapes, sections",          2.01, False),
    ("7217", "Iron & Steel", "Wire of iron or non-alloy steel",   2.12, False),
    ("7218", "Iron & Steel", "Stainless steel semi-finished",     2.21, False),
    ("7219", "Iron & Steel", "Stainless steel flat-rolled (hot)", 2.21, False),
    ("7220", "Iron & Steel", "Stainless steel flat-rolled (cold)",2.31, False),
    ("7221", "Iron & Steel", "Stainless steel bars (hot-rolled)", 2.21, False),
    ("7222", "Iron & Steel", "Stainless steel bars (other)",      2.21, False),
    ("7223", "Iron & Steel", "Stainless steel wire",              2.31, False),
    ("7224", "Iron & Steel", "Other alloy steel semi-finished",   2.10, False),
    ("7225", "Iron & Steel", "Other alloy steel flat-rolled",     2.10, False),
    ("7226", "Iron & Steel", "Other alloy steel flat-rolled <600",2.10, False),
    ("7227", "Iron & Steel", "Other alloy steel bars (hot-rolled)",2.10, False),
    ("7228", "Iron & Steel", "Other alloy steel bars/angles",     2.10, False),
    ("7229", "Iron & Steel", "Other alloy steel wire",            2.20, False),
    ("73",   "Iron & Steel", "Articles of iron or steel",         2.01, False),
    ("7301", "Iron & Steel", "Sheet piling",                      2.01, False),
    ("7302", "Iron & Steel", "Railway track construction material",2.01, False),
    ("7303", "Iron & Steel", "Tubes and pipes (cast iron)",       2.01, False),
    ("7304", "Iron & Steel", "Tubes and pipes (seamless)",        2.30, False),
    ("7305", "Iron & Steel", "Tubes and pipes (welded > 406mm)",  2.20, False),
    ("7306", "Iron & Steel", "Tubes and pipes (welded other)",    2.20, False),
    ("7307", "Iron & Steel", "Tube/pipe fittings",                2.20, False),
    ("7308", "Iron & Steel", "Structures and parts",              2.20, False),
    ("7309", "Iron & Steel", "Reservoirs, tanks, vats > 300L",    2.20, False),
    ("7310", "Iron & Steel", "Tanks, casks, drums <= 300L",       2.20, False),
    ("7311", "Iron & Steel", "Containers for compressed gas",     2.30, False),
    ("7318", "Iron & Steel", "Screws, bolts, nuts, washers",      2.50, False),
    ("7326", "Iron & Steel", "Other articles of iron or steel",   2.20, False),
    ("26",   "Iron & Steel", "Iron ores and concentrates",        0.07, False),

    # Aluminium (direct emissions only)
    ("76",   "Aluminium", "Aluminium and articles thereof",       2.36, False),
    ("7601", "Aluminium", "Unwrought aluminium",                  2.36, False),
    ("7602", "Aluminium", "Aluminium waste and scrap",            0.60, False),
    ("7603", "Aluminium", "Aluminium powders and flakes",         2.50, False),
    ("7604", "Aluminium", "Aluminium bars, rods, profiles",       2.60, False),
    ("7605", "Aluminium", "Aluminium wire",                       2.60, False),
    ("7606", "Aluminium", "Aluminium plates, sheets, strip",      2.70, False),
    ("7607", "Aluminium", "Aluminium foil",                       2.80, False),
    ("7608", "Aluminium", "Aluminium tubes and pipes",            2.70, False),
    ("7609", "Aluminium", "Aluminium tube/pipe fittings",         2.70, False),
    ("7610", "Aluminium", "Aluminium structures and parts",       2.70, False),
    ("7611", "Aluminium", "Aluminium reservoirs/tanks > 300L",    2.70, False),
    ("7612", "Aluminium", "Aluminium casks/drums <= 300L",        2.70, False),
    ("7613", "Aluminium", "Aluminium containers (compressed gas)",2.80, False),
    ("7614", "Aluminium", "Stranded wire/cables",                 2.60, False),
    ("7616", "Aluminium", "Other articles of aluminium",          2.70, False),

    # Cement (direct + indirect emissions)
    ("2507", "Cement", "Calcined kaolinic clays",                 0.53, True),
    ("2523", "Cement", "Portland cement",                         0.87, True),
    ("252310","Cement", "Cement clinkers",                         0.93, True),
    ("252321","Cement", "White Portland cement",                   0.87, True),
    ("252329","Cement", "Other Portland cement",                   0.87, True),
    ("252330","Cement", "Aluminous cement",                        0.87, True),
    ("252390","Cement", "Other hydraulic cements",                 0.73, True),

    # Fertilisers (direct + indirect emissions)
    ("2808", "Fertilisers", "Nitric acid",                        1.61, True),
    ("2814", "Fertilisers", "Ammonia",                            2.82, True),
    ("2834", "Fertilisers", "Nitrites and nitrates",              1.70, True),
    ("3102", "Fertilisers", "Mineral/chemical nitrogen fertilisers",1.70, True),
    ("310210","Fertilisers","Urea",                               2.82, True),
    ("310221","Fertilisers","Ammonium sulphate",                   1.95, True),
    ("310230","Fertilisers","Ammonium nitrate",                    2.56, True),
    ("310240","Fertilisers","Ammonium nitrate + calcium carbonate",2.00, True),
    ("310250","Fertilisers","Sodium nitrate",                      1.70, True),
    ("310260","Fertilisers","Calcium cyanamide (double salts)",    1.70, True),
    ("310280","Fertilisers","Urea + ammonium nitrate (UAN)",       2.69, True),
    ("310290","Fertilisers","Other nitrogen fertilisers",          1.70, True),
    ("3105", "Fertilisers", "Mineral/chemical fertilisers (mixed)",1.96, True),
    ("310510","Fertilisers","NPK-type fertilisers",               1.96, True),
    ("310520","Fertilisers","NP/NK/PK fertilisers",               1.80, True),
    ("310590","Fertilisers","Other fertilisers",                   1.80, True),

    # Hydrogen (direct emissions only)
    ("280410","Hydrogen", "Hydrogen",                             10.40, False),

    # Electricity (direct emissions only — grid default)
    ("2716",  "Electricity", "Electrical energy",                  0.45, False),
]

# Definitive-period markup schedule per Art. 7
YEAR_MARKUPS = {
    2026: 0.10,
    2027: 0.20,
    2028: 0.30,
    2029: 0.30,
    2030: 0.30,
    2031: 0.30,
    2032: 0.30,
    2033: 0.30,
    2034: 0.30,
}

SOURCE = "EC Implementing Regulation 2023/1773 + Definitive-period markup per Regulation 2023/956 Art. 7"


def seed():
    db = SessionLocal()
    try:
        # Clear existing data
        existing = db.query(CBAMDefault).count()
        if existing > 0:
            print(f"Clearing {existing} existing rows...")
            db.query(CBAMDefault).delete()
            db.commit()

        rows_added = 0
        for year, markup in YEAR_MARKUPS.items():
            for cn_prefix, sector, desc, base_val, incl_indirect in BASE_DEFAULTS:
                effective = round(base_val * (1 + markup), 4)
                row = CBAMDefault(
                    cn_prefix=cn_prefix,
                    sector=sector,
                    product_description=desc,
                    origin_country=None,  # Global default (all countries)
                    year=year,
                    base_value=base_val,
                    markup_pct=markup,
                    effective_value=effective,
                    includes_indirect=incl_indirect,
                    source=SOURCE,
                )
                db.add(row)
                rows_added += 1

        db.commit()
        print(f"✓ Seeded {rows_added} rows ({len(BASE_DEFAULTS)} CN prefixes × {len(YEAR_MARKUPS)} years)")
        
        # Verify
        sample = db.query(CBAMDefault).filter(
            CBAMDefault.cn_prefix == "7208",
            CBAMDefault.year == 2026
        ).first()
        if sample:
            print(f"  Sample: CN 7208 (Hot-rolled steel) in 2026 = {sample.effective_value} tCO2/t "
                  f"(base {sample.base_value} + {int(sample.markup_pct*100)}% markup)")

        sample2 = db.query(CBAMDefault).filter(
            CBAMDefault.cn_prefix == "280410",
            CBAMDefault.year == 2027
        ).first()
        if sample2:
            print(f"  Sample: CN 280410 (Hydrogen) in 2027 = {sample2.effective_value} tCO2/t "
                  f"(base {sample2.base_value} + {int(sample2.markup_pct*100)}% markup)")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
