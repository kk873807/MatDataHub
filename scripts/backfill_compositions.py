import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import Material

compositions = {
    "Inconel 718": "Ni 50-55%, Cr 17-21%, Fe Balance, Nb 4.7-5.5%, Mo 2.8-3.3%",
    "Inconel 625": "Ni 58% min, Cr 20-23%, Mo 8-10%, Fe 5% max, Nb 3.15-4.15%",
    "Aluminum 6061-T6": "Al 95.8-98.6%, Mg 0.8-1.2%, Si 0.4-0.8%, Cu 0.15-0.4%",
    "Aluminum 7075-T6": "Al 87.1-91.4%, Zn 5.1-6.1%, Mg 2.1-2.9%, Cu 1.2-2.0%",
    "Aluminum 2024-T3": "Al 90.7-94.7%, Cu 3.8-4.9%, Mg 1.2-1.8%, Mn 0.3-0.9%",
    "Aluminum 5052-H32": "Al 95.7-97.7%, Mg 2.2-2.8%, Cr 0.15-0.35%",
    "Aluminum 1100-H14": "Al 99.0% min, Cu 0.05-0.20%, Zn 0.10% max"
}

def backfill():
    db = SessionLocal()
    updated = 0
    for name, comp in compositions.items():
        mat = db.query(Material).filter(Material.name == name).first()
        if mat:
            mat.composition = comp
            updated += 1
    
    db.commit()
    db.close()
    print(f"Backfilled composition data for {updated} materials.")

if __name__ == "__main__":
    backfill()
