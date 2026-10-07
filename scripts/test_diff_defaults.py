import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import func

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal, engine
from app.models import CBAMDefault

def main():
    db = SessionLocal()
    
    total = db.query(CBAMDefault).count()
    print(f"Total rows in CBAMDefault: {total}")
    assert total > 10000, f"Expected >10,000 default entries, found {total}"
    
    countries = db.query(CBAMDefault.origin_country).distinct().count()
    print(f"Number of distinct countries/origins: {countries}")
    assert countries > 50, f"Expected >50 countries, found {countries}"
    
    # Check China Rebar (72142000) 2026
    china_rebar = db.query(CBAMDefault).filter_by(
        origin_country="China", 
        cn_prefix="72142000", 
        year=2026
    ).first()
    
    assert china_rebar is not None, "China rebar (72142000) not found for 2026"
    assert china_rebar.sector == "Iron & Steel"
    
    # Verify Steel markup is 10% (0.1) in 2026
    assert abs(china_rebar.markup_pct - 0.1) < 0.001, f"Expected 10% markup, got {china_rebar.markup_pct}"
    expected_eff = china_rebar.base_value * 1.10
    assert abs(china_rebar.effective_value - expected_eff) < 0.001
    print(f"✓ China Rebar 72142000 2026 base={china_rebar.base_value:.3f}, eff={china_rebar.effective_value:.3f}")
    
    # Check Fertilizer markup is 1% (0.01) in 2026
    fert = db.query(CBAMDefault).filter(
        CBAMDefault.sector == "Fertilisers",
        CBAMDefault.year == 2026
    ).first()
    assert fert is not None, "No fertilizer found"
    assert abs(fert.markup_pct - 0.01) < 0.001, f"Expected 1% markup for fertiliser, got {fert.markup_pct}"
    
    # Check UNKNOWN_ORIGIN exists
    unknown = db.query(CBAMDefault).filter_by(origin_country="UNKNOWN_ORIGIN").count()
    print(f"UNKNOWN_ORIGIN rows: {unknown}")
    assert unknown > 100, f"Expected >100 unknown origin rows from Annex IV, found {unknown}"
    
    # Check that highest default values are indeed higher or equal to country specific
    # (Just a basic check on a known code)
    rebar_unknown = db.query(CBAMDefault).filter_by(
        origin_country="UNKNOWN_ORIGIN", 
        cn_prefix="72142000", 
        year=2026
    ).first()
    if rebar_unknown:
        print(f"✓ Unknown Rebar 7214 2026 base={rebar_unknown.base_value:.3f}, eff={rebar_unknown.effective_value:.3f}")
        assert rebar_unknown.base_value >= china_rebar.base_value, "Fallback should be >= country specific"
    
    print("\nAll diff tests passed!")

if __name__ == "__main__":
    main()
