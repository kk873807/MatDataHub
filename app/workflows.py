import pandas as pd
import math
from thefuzz import process
from sqlalchemy.orm import Session
from app.models import Material

class SubstitutionEngine:
    """
    Engine to find alternative materials based on multi-objective weighted parameters.
    Targeted at Pro users.
    """
    def __init__(self, db: Session):
        self.db = db

    def find_alternatives(self, base_material_id: int, weights: dict, limit: int = 5):
        """
        weights: dict like {'cost': 0.8, 'density': 1.0, 'tensile_strength': 0.5, 'embodied_carbon': 0.3}
        Scale: 0.0 to 1.0
        """
        base = self.db.query(Material).filter(Material.id == base_material_id).first()
        if not base:
            return []

        candidates = self.db.query(Material).filter(
            Material.category == base.category,
            Material.id != base.id
        ).all()

        def extract_features(m):
            cost = m.cost_per_kg_min if m.cost_per_kg_min else 100.0
            density = m.density if m.density else 5.0
            tensile = m.tensile_strength_min if m.tensile_strength_min else 100.0
            carbon = m.embodied_carbon if m.embodied_carbon else 5.0
            return cost, density, tensile, carbon

        b_cost, b_density, b_tensile, b_carbon = extract_features(base)
        
        max_cost = max([extract_features(c)[0] for c in candidates] + [b_cost, 0.1])
        max_density = max([extract_features(c)[1] for c in candidates] + [b_density, 0.1])
        max_tensile = max([extract_features(c)[2] for c in candidates] + [b_tensile, 0.1])
        max_carbon = max([extract_features(c)[3] for c in candidates] + [b_carbon, 0.1])

        results = []
        for c in candidates:
            c_cost, c_density, c_tensile, c_carbon = extract_features(c)
            
            diff_cost = ((c_cost - b_cost) / max_cost) * weights.get('cost', 1.0)
            diff_density = ((c_density - b_density) / max_density) * weights.get('density', 1.0)
            diff_tensile = ((c_tensile - b_tensile) / max_tensile) * weights.get('tensile_strength', 1.0)
            diff_carbon = ((c_carbon - b_carbon) / max_carbon) * weights.get('embodied_carbon', 1.0)
            
            distance = math.sqrt(diff_cost**2 + diff_density**2 + diff_tensile**2 + diff_carbon**2)
            
            max_possible_dist = math.sqrt(sum([w**2 for w in weights.values()])) if weights else 2.0
            match_score = max(0, 100 - (distance / max_possible_dist) * 100)
            
            results.append({
                "material": c,
                "distance": distance,
                "match_score": round(match_score, 1)
            })

        results.sort(key=lambda x: x["distance"])
        return results[:limit]


# Industry-standard fallback emission factors (kg CO2e per kg of material)
# Sources: ICE Database v3 (University of Bath), EU CBAM default values
FALLBACK_CARBON_FACTORS = {
    "stainless steel": 6.15, "carbon steel": 1.85, "steel": 1.85,
    "aluminium": 8.24, "aluminum": 8.24,
    "copper": 3.81, "brass": 3.50, "bronze": 3.70,
    "titanium": 35.7, "nickel": 12.4, "zinc": 3.86,
    "magnesium": 8.10, "iron": 1.91, "cast iron": 1.91,
    "lead": 1.57, "tin": 14.5,
    "nylon": 8.50, "polyethylene": 1.94, "polypropylene": 1.95,
    "pvc": 2.41, "polycarbonate": 7.62, "abs": 3.76,
    "epoxy": 6.70, "polyester": 2.70, "rubber": 3.18,
    "ptfe": 10.2, "peek": 26.4, "polymer": 3.40, "plastic": 3.40,
    "ceramic": 0.70, "glass": 0.86, "concrete": 0.13,
    "cement": 0.83, "alumina": 3.68, "silicon carbide": 4.20, "zirconia": 3.90,
    "carbon fiber": 29.5, "fiberglass": 8.10, "gfrp": 8.10, "cfrp": 29.5,
    "composite": 5.50,
}

CBAM_REFERENCE_PRICE_EUR = 75.0


def _estimate_carbon_factor(material_name, category=""):
    name_lower = material_name.lower()
    sorted_keys = sorted(FALLBACK_CARBON_FACTORS.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in name_lower:
            return FALLBACK_CARBON_FACTORS[key]
    cat_lower = (category or "").lower()
    cat_defaults = {"metal": 3.50, "polymer": 3.40, "ceramic": 1.20, "composite": 5.50}
    for ck, dv in cat_defaults.items():
        if ck in cat_lower:
            return dv
    return 2.50


class BOMProcessor:
    def __init__(self, db: Session):
        self.db = db
        all_mats = self.db.query(Material.id, Material.name).all()
        self.mat_dict = {m.id: m.name for m in all_mats}
        self.mat_names = list(self.mat_dict.values())

    def process_bom(self, df, material_col, weight_col):
        enriched_rows = []
        for index, row in df.iterrows():
            raw_name = str(row.get(material_col, ""))
            weight_kg = float(row.get(weight_col, 0.0)) if pd.notna(row.get(weight_col)) else 0.0
            if not raw_name:
                continue
            match_tuple = process.extractOne(raw_name, self.mat_names)
            if match_tuple and match_tuple[1] > 60:
                matched_name = match_tuple[0]
                confidence = match_tuple[1]
                mat = self.db.query(Material).filter(Material.name == matched_name).first()
                db_carbon = mat.embodied_carbon if mat.embodied_carbon else 0.0
                carbon_factor = db_carbon if db_carbon > 0 else _estimate_carbon_factor(mat.name, mat.category)
                total_co2_kg = round(weight_kg * carbon_factor, 3)
                total_co2_tonnes = total_co2_kg / 1000.0
                cbam_cost_eur = round(total_co2_tonnes * CBAM_REFERENCE_PRICE_EUR, 2)
                obsolete_flag = "YES" if mat.is_obsolete else "NO"
                replacement = mat.replacement_standard if mat.replacement_standard else "N/A"
                carbon_score = min(carbon_factor / 30.0 * 50, 50)
                recyclability = mat.recyclability_index if mat.recyclability_index else 0.5
                recycle_score = (1 - recyclability) * 30
                obsolete_score = 20 if mat.is_obsolete else 0
                esg_risk = round(min(carbon_score + recycle_score + obsolete_score, 100), 1)
                enriched_rows.append({
                    **row.to_dict(),
                    "Matched_Material": mat.name,
                    "Match_Confidence": f"{confidence}%",
                    "Carbon_Factor_kgCO2e_per_kg": round(carbon_factor, 3),
                    "Total_CO2_kg": round(total_co2_kg, 3),
                    "Total_CO2_tonnes": round(total_co2_tonnes, 4),
                    "CBAM_Cost_EUR": cbam_cost_eur,
                    "Is_Obsolete": obsolete_flag,
                    "Replacement_Standard": replacement,
                    "ESG_Risk_Score": esg_risk,
                })
            else:
                enriched_rows.append({
                    **row.to_dict(),
                    "Matched_Material": "NO MATCH FOUND",
                    "Match_Confidence": "0%",
                    "Carbon_Factor_kgCO2e_per_kg": 0.0,
                    "Total_CO2_kg": 0.0,
                    "Total_CO2_tonnes": 0.0,
                    "CBAM_Cost_EUR": 0.0,
                    "Is_Obsolete": "N/A",
                    "Replacement_Standard": "N/A",
                    "ESG_Risk_Score": 0.0,
                })
        return pd.DataFrame(enriched_rows)
