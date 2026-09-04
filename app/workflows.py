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

        # Get all materials in the same category (e.g. Metal) to compare apples to apples
        candidates = self.db.query(Material).filter(
            Material.category == base.category,
            Material.id != base.id
        ).all()

        # Extract features for normalization
        def extract_features(m):
            # Fallback to sensible defaults if null (for distance calc)
            cost = m.cost_per_kg_min if m.cost_per_kg_min else 100.0
            density = m.density if m.density else 5.0
            tensile = m.tensile_strength_min if m.tensile_strength_min else 100.0
            carbon = m.embodied_carbon if m.embodied_carbon else 5.0
            return cost, density, tensile, carbon

        b_cost, b_density, b_tensile, b_carbon = extract_features(base)
        
        # We need max values to normalize between 0 and 1
        max_cost = max([extract_features(c)[0] for c in candidates] + [b_cost, 0.1])
        max_density = max([extract_features(c)[1] for c in candidates] + [b_density, 0.1])
        max_tensile = max([extract_features(c)[2] for c in candidates] + [b_tensile, 0.1])
        max_carbon = max([extract_features(c)[3] for c in candidates] + [b_carbon, 0.1])

        results = []
        for c in candidates:
            c_cost, c_density, c_tensile, c_carbon = extract_features(c)
            
            # Normalize differences
            diff_cost = ((c_cost - b_cost) / max_cost) * weights.get('cost', 1.0)
            diff_density = ((c_density - b_density) / max_density) * weights.get('density', 1.0)
            diff_tensile = ((c_tensile - b_tensile) / max_tensile) * weights.get('tensile_strength', 1.0)
            diff_carbon = ((c_carbon - b_carbon) / max_carbon) * weights.get('embodied_carbon', 1.0)
            
            # Euclidean distance
            distance = math.sqrt(diff_cost**2 + diff_density**2 + diff_tensile**2 + diff_carbon**2)
            
            # Convert distance to a "Match Score" (0 to 100%)
            # Max possible distance theoretically is sqrt(4) = 2 if everything is 1.0 vs 0.0 and weights are 1.0
            max_possible_dist = math.sqrt(sum([w**2 for w in weights.values()])) if weights else 2.0
            match_score = max(0, 100 - (distance / max_possible_dist) * 100)
            
            results.append({
                "material": c,
                "distance": distance,
                "match_score": round(match_score, 1)
            })

        # Sort by distance (lowest is best)
        results.sort(key=lambda x: x["distance"])
        return results[:limit]


class BOMProcessor:
    """
    Enterprise tool to ingest a CSV/Excel Bill of Materials, map to exact materials,
    check obsolescence, and calculate carbon footprint.
    """
    def __init__(self, db: Session):
        self.db = db
        # Pre-load material names for fuzzy matching
        all_mats = self.db.query(Material.id, Material.name).all()
        self.mat_dict = {m.id: m.name for m in all_mats}
        self.mat_names = list(self.mat_dict.values())

    def process_bom(self, df: pd.DataFrame, material_col: str, weight_col: str):
        """
        Takes a pandas DataFrame and enriches it.
        material_col: Column name containing the messy material string
        weight_col: Column name containing the weight in kg per part
        """
        enriched_rows = []
        
        for index, row in df.iterrows():
            raw_name = str(row.get(material_col, ""))
            weight_kg = float(row.get(weight_col, 0.0)) if pd.notna(row.get(weight_col)) else 0.0
            
            if not raw_name:
                continue
                
            # 1. Fuzzy Match
            match_tuple = process.extractOne(raw_name, self.mat_names)
            if match_tuple and match_tuple[1] > 60: # Threshold
                matched_name = match_tuple[0]
                confidence = match_tuple[1]
                
                # Fetch exact material
                mat = self.db.query(Material).filter(Material.name == matched_name).first()
                
                # 2. Extract Data
                obsolete_flag = "YES" if mat.is_obsolete else "NO"
                replacement = mat.replacement_standard if mat.replacement_standard else "N/A"
                carbon_factor = mat.embodied_carbon if mat.embodied_carbon else 0.0
                total_carbon = round(weight_kg * carbon_factor, 2)
                
                enriched_rows.append({
                    **row.to_dict(), # Keep original columns
                    "Matched_Material": mat.name,
                    "Match_Confidence": f"{confidence}%",
                    "Is_Obsolete": obsolete_flag,
                    "Replacement_Standard": replacement,
                    "Embodied_Carbon_Factor": carbon_factor,
                    "Total_Carbon_kgCO2e": total_carbon
                })
            else:
                enriched_rows.append({
                    **row.to_dict(),
                    "Matched_Material": "NO MATCH FOUND",
                    "Match_Confidence": "0%",
                    "Is_Obsolete": "N/A",
                    "Replacement_Standard": "N/A",
                    "Embodied_Carbon_Factor": 0.0,
                    "Total_Carbon_kgCO2e": 0.0
                })
                
        return pd.DataFrame(enriched_rows)
