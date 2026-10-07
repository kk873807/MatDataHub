"""
Parse the official EUR-Lex HTML of Regulation (EU) 2026/1740 and seed the database.
Handles Annex I (country-specific) and Annex IV (highest defaults).
"""
import re
import sys
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine, SessionLocal, Base
from app.models import CBAMDefault

HTML_PATH = "data/cbam_official/32026R1740.html"

# Mark-ups defined in the Regulation text
MARKUPS = {
    "Fertilisers": {2026: 0.01, 2027: 0.01, 2028: 0.01, 2029: 0.01, 2030: 0.01, 2031: 0.01, 2032: 0.01, 2033: 0.01, 2034: 0.01},
    "default": {2026: 0.10, 2027: 0.20, 2028: 0.30, 2029: 0.30, 2030: 0.30, 2031: 0.30, 2032: 0.30, 2033: 0.30, 2034: 0.30}
}

def parse_float_eu(val: str) -> float:
    """Parse EU decimal comma (e.g. '1,230') to float."""
    v = val.strip().replace("\xa0", "")
    if v in ("-", "N/A", "", "see below"):
        return 0.0
    return float(v.replace(",", "."))

def main():
    if not os.path.exists(HTML_PATH):
        sys.exit(f"File not found: {HTML_PATH}. Run fetch_cbam_official.py first.")

    print("Parsing HTML...")
    with open(HTML_PATH, encoding="utf-8", errors="replace") as f:
        html = f.read()
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    existing = db.query(CBAMDefault).count()
    if existing > 0:
        print(f"Clearing {existing} existing rows...")
        db.query(CBAMDefault).delete()
        db.commit()

    rows_added = 0
    current_sector = "Unknown"
    
    for t in tables:
        rows = t.find_all("tr")
        ncols = max((len(r.find_all(["td", "th"])) for r in rows), default=0)
        
        if ncols == 6:
            # Annex I: Country tables
            cells = [c.get_text(" ", strip=True) for c in rows[0].find_all(["td", "th"])]
            country = cells[0].strip() if len(cells) == 1 else ""
            if "Product CN Code" in country or not country:
                continue
                
            if country.lower() == "other countries and territories":
                country = None  # Global fallback
                
            for r in rows[1:]:
                cells = [c.get_text(" ", strip=True) for c in r.find_all(["td", "th"])]
                if len(cells) != 6: continue
                
                cn_raw = cells[0].strip()
                desc = cells[1].strip()
                direct_str = cells[2]
                indirect_str = cells[3]
                total_str = cells[4]
                route = cells[5].strip()
                
                if "Product CN Code" in cn_raw: continue
                
                if not desc and not direct_str and not total_str:
                    # It's a sector header row (e.g., 'Cement', 'Fertilisers')
                    if cn_raw in ["Cement", "Iron and steel", "Aluminium", "Fertilisers", "Hydrogen"]:
                        current_sector = cn_raw
                        if current_sector == "Iron and steel": current_sector = "Iron & Steel"
                    continue
                    
                code = re.sub(r"\D", "", cn_raw)
                if not code: continue
                
                total_val = parse_float_eu(total_str)
                indirect_val = parse_float_eu(indirect_str)
                includes_indirect = (indirect_val > 0)
                
                if total_val == 0.0: continue # E.g., "-" means no default value
                
                markup_schedule = MARKUPS["Fertilisers"] if current_sector == "Fertilisers" else MARKUPS["default"]
                
                for year, markup in markup_schedule.items():
                    db.add(CBAMDefault(
                        cn_prefix=code,
                        sector=current_sector,
                        product_description=desc,
                        origin_country=country,
                        year=year,
                        base_value=total_val,
                        markup_pct=markup,
                        effective_value=total_val * (1.0 + markup),
                        includes_indirect=includes_indirect,
                        source="Commission Implementing Regulation (EU) 2026/1740 (Annex I)"
                    ))
                    rows_added += 1

        elif ncols == 4:
            # Annex IV: Highest default values (used when origin is entirely unknown)
            prev = t.find_previous(string=re.compile(r"highest default values", re.I))
            if not prev: continue
            
            country = "UNKNOWN_ORIGIN"
            for r in rows:
                cells = [c.get_text(" ", strip=True) for c in r.find_all(["td", "th"])]
                if len(cells) != 4: continue
                
                cn_raw = cells[0].strip()
                desc = cells[1].strip()
                total_str = cells[2]
                route = cells[3].strip()
                
                if "Product CN Code" in cn_raw: continue
                if not desc and not total_str:
                    if cn_raw in ["Cement", "Iron and steel", "Aluminium", "Fertilisers", "Hydrogen"]:
                        current_sector = cn_raw
                        if current_sector == "Iron and steel": current_sector = "Iron & Steel"
                    continue
                    
                code = re.sub(r"\D", "", cn_raw)
                if not code: continue
                
                total_val = parse_float_eu(total_str)
                if total_val == 0.0: continue
                
                # Assume includes_indirect based on sector for the "highest" fallback
                includes_indirect = current_sector in ["Cement", "Fertilisers"]
                
                markup_schedule = MARKUPS["Fertilisers"] if current_sector == "Fertilisers" else MARKUPS["default"]
                
                for year, markup in markup_schedule.items():
                    db.add(CBAMDefault(
                        cn_prefix=code,
                        sector=current_sector,
                        product_description=desc,
                        origin_country=country,
                        year=year,
                        base_value=total_val,
                        markup_pct=markup,
                        effective_value=total_val * (1.0 + markup),
                        includes_indirect=includes_indirect,
                        source="Commission Implementing Regulation (EU) 2026/1740 (Annex IV)"
                    ))
                    rows_added += 1

    db.commit()
    print(f"✓ Seeded {rows_added} rows into cbam_defaults.")
    
if __name__ == "__main__":
    main()
