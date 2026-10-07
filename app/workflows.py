import pandas as pd
import math
import datetime
import re
from thefuzz import process, fuzz
from collections import defaultdict
from sqlalchemy.orm import Session
from app.models import Material, CBAMDefault

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
    # CBAM-covered sectors: EU default values (direct emissions only, except cement/fertiliser)
    "hydrogen": 10.4,
    "ammonia": 2.82, "urea": 2.82,
    "stainless steel": 2.21, "carbon steel": 2.01, "steel": 2.01,
    "aluminium": 2.36, "aluminum": 2.36,
    "iron": 2.01, "cast iron": 2.01,
    "cement": 0.87, "clinker": 0.87,
    "fertiliser": 3.0, "fertilizer": 3.0,
    # Non-CBAM materials: lifecycle-based estimates for ESG scoring only
    "copper": 3.81, "brass": 3.50, "bronze": 3.70,
    "titanium": 35.7, "nickel": 12.4, "zinc": 3.86,
    "magnesium": 8.10, "lead": 1.57, "tin": 14.5,
    "nylon": 8.50, "polyethylene": 1.94, "polypropylene": 1.95,
    "pvc": 2.41, "polycarbonate": 7.62, "abs": 3.76,
    "epoxy": 6.70, "polyester": 2.70, "rubber": 3.18,
    "ptfe": 10.2, "peek": 26.4, "polymer": 3.40, "plastic": 3.40,
    "ceramic": 0.70, "glass": 0.86, "concrete": 0.13,
    "alumina": 3.68, "silicon carbide": 4.20, "zirconia": 3.90,
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
    EU_EEA_COUNTRIES = {
        'austria', 'belgium', 'bulgaria', 'croatia', 'republic of cyprus', 'cyprus', 'czech republic', 'czechia',
        'denmark', 'estonia', 'finland', 'france', 'germany', 'greece', 'hungary', 'ireland', 'italy',
        'latvia', 'lithuania', 'luxembourg', 'malta', 'netherlands', 'poland', 'portugal', 'romania',
        'slovakia', 'slovenia', 'spain', 'sweden',
        'iceland', 'liechtenstein', 'norway', 'switzerland'
    }
    
    EU_DESTINATION_COUNTRIES = {
        'austria', 'belgium', 'bulgaria', 'croatia', 'republic of cyprus', 'cyprus', 'czech republic', 'czechia',
        'denmark', 'estonia', 'finland', 'france', 'germany', 'greece', 'hungary', 'ireland', 'italy',
        'latvia', 'lithuania', 'luxembourg', 'malta', 'netherlands', 'poland', 'portugal', 'romania',
        'slovakia', 'slovenia', 'spain', 'sweden'
    }

    # Minimum candidate name length to prevent 2-3 letter element symbols
    # (e.g. Ga, Li, Ni, Re, Ir) from winning fuzzy matches via trivial substrings
    MIN_CANDIDATE_LENGTH = 4

    # Map CBAM sector keywords → Material.category values for pre-filtering
    CBAM_SECTOR_CATEGORY_MAP = {
        "iron": ["Metal"],
        "steel": ["Metal"],
        "iron & steel": ["Metal"],
        "iron and steel": ["Metal"],
        "cement": ["Ceramic"],  # Cement/clinker stored under Ceramic
        "aluminium": ["Metal"],
        "aluminum": ["Metal"],
        "fertiliser": [],       # No natural DB category — skip pre-filter
        "fertilizer": [],
        "hydrogen": [],
        "electricity": [],         # No natural DB category — skip pre-filter
    }
    
    # ── Annex I Rule Table (Regulation (EU) 2023/956) ──
    # Evaluated top-down; first matching prefix wins.
    # Rules list the exact string prefix to match.
    ANNEX_I_RULES = [
        # Explicit exclusions in Chapter 72
        ("72022", "exclude", None),        # Ferro-silicon
        ("7204", "exclude", None),         # Ferrous waste and scrap

        # Cement
        ("25070080", "include", "cement"), # Kaolinitic clays
        ("25231000", "include", "cement"),
        ("25232100", "include", "cement"),
        ("25232900", "include", "cement"),
        ("25233000", "include", "cement"),
        ("25239000", "include", "cement"),

        # Electricity
        ("27160000", "include", "electricity"),

        # Hydrogen
        ("28041000", "include", "hydrogen"),

        # Fertilisers
        ("28080000", "include", "fertiliser"),
        ("2814", "include", "fertiliser"),
        ("28342100", "include", "fertiliser"),
        ("3102", "include", "fertiliser"),
        ("31056000", "exclude", None),     # Excluded from 3105
        ("3105", "include", "fertiliser"),

        # Iron ores (agglomerated)
        ("26011200", "include", "iron & steel"),

        # Iron & Steel: Chapter 72 (after exclusions)
        ("72", "include", "iron & steel"),

        # Iron & Steel: Chapter 73
        ("7301", "include", "iron & steel"),
        ("7302", "include", "iron & steel"),
        ("730300", "include", "iron & steel"),
        ("7304", "include", "iron & steel"),
        ("7305", "include", "iron & steel"),
        ("7306", "include", "iron & steel"),
        ("7307", "include", "iron & steel"),
        ("7308", "include", "iron & steel"),
        ("730900", "include", "iron & steel"),
        ("7310", "include", "iron & steel"),
        ("731100", "include", "iron & steel"),
        ("7318", "include", "iron & steel"),
        ("7326", "include", "iron & steel"),

        # Aluminium
        ("7602", "exclude", None),         # Waste and scrap
        ("7601", "include", "aluminium"),
        ("7603", "include", "aluminium"),
        ("7604", "include", "aluminium"),
        ("7605", "include", "aluminium"),
        ("7606", "include", "aluminium"),
        ("7607", "include", "aluminium"),
        ("7608", "include", "aluminium"),
        ("76090000", "include", "aluminium"),
        ("7610", "include", "aluminium"),
        ("76110000", "include", "aluminium"),
        ("7612", "include", "aluminium"),
        ("76130000", "include", "aluminium"),
        ("7614", "include", "aluminium"),
        ("76169990", "include", "aluminium"),
    ]

    @classmethod
    def get_sector_from_cn(cls, clean_cn: str):
        """
        Data-driven Annex I lookup returning a detailed status.
        Returns (status, sector)
        status in ["EXACT_MATCH", "EXCLUDED", "INCOMPLETE", "NOT_COVERED"]
        """
        if not clean_cn:
            return ("NOT_COVERED", None)
            
        # 1. Find what the input WOULD match if it were fully specified
        matched_action = "not_covered"
        matched_sector = None
        for prefix, action, sector in cls.ANNEX_I_RULES:
            if clean_cn.startswith(prefix):
                matched_action = action
                matched_sector = sector
                break
                
        # 2. Check for ambiguity: does any longer rule (that extends our input) have a DIFFERENT action?
        # E.g. input `3105` matches `3105` (include), but `31056000` (exclude) extends it.
        # E.g. input `7202` matches `72` (include), but `72022` (exclude) extends it.
        # E.g. input `2507` matches nothing (not_covered), but `25070080` (include) extends it.
        for prefix, action, sector in cls.ANNEX_I_RULES:
            if prefix.startswith(clean_cn) and len(prefix) > len(clean_cn):
                if action != matched_action:
                    # Ambiguous! We need more digits.
                    return ("INCOMPLETE", sector if action == "include" else matched_sector)
                    
        # 3. If no ambiguity, return the matched outcome
        if matched_action == "not_covered":
            return ("NOT_COVERED", None)
        elif matched_action == "exclude":
            return ("EXCLUDED", None)
        else:
            return ("EXACT_MATCH", matched_sector)

    # Country name aliases for normalisation
    COUNTRY_ALIASES = {
        "usa": "united states", "united states of america": "united states",
        "uk": "united kingdom", "great britain": "united kingdom",
        "the netherlands": "netherlands",
        "viet nam": "vietnam", "vn": "vietnam",
        "turkiye": "turkey", "türkiye": "turkey",
        "republic of korea": "south korea", "korea": "south korea",
        "prc": "china", "peoples republic of china": "china",
        "uae": "united arab emirates",
        "russian federation": "russia",
    }

    def __init__(self, db: Session):
        self.db = db
        all_mats = self.db.query(Material.id, Material.name, Material.category, Material.embodied_carbon, Material.is_obsolete, Material.replacement_standard, Material.recyclability_index).all()
        self.mat_dict = {m.name: m for m in all_mats}
        self.mat_names = [m.name for m in all_mats if len(m.name) >= self.MIN_CANDIDATE_LENGTH]
        # Build category → [name, ...] for sector-aware pre-filtering
        self.cat_to_names = {}
        for m in all_mats:
            if len(m.name) >= self.MIN_CANDIDATE_LENGTH:
                cat = (m.category or "").strip()
                self.cat_to_names.setdefault(cat, []).append(m.name)
        
        # Per-instance fuzzy match cache (avoids lru_cache keying on self)
        self._match_cache = {}
        
        # Preload CBAM defaults into memory for fast lookups
        self.cbam_defaults_cache = {}
        self.cbam_defaults_stale = False
        self.cbam_defaults_count = 0
        self.cbam_defaults_version = None
        self.cbam_defaults_load_error = None

        try:
            all_defaults = self.db.query(CBAMDefault).all()
            for d in all_defaults:
                key = (d.cn_prefix, d.year, (d.origin_country or "").lower() if d.origin_country else None)
                self.cbam_defaults_cache[key] = d
            self.cbam_defaults_count = len(all_defaults)
            if all_defaults:
                latest = max(d.updated_at for d in all_defaults if d.updated_at)
                self.cbam_defaults_version = latest.isoformat() if latest else None
                if latest and (datetime.datetime.now(latest.tzinfo) - latest).days > 90:
                    self.cbam_defaults_stale = True
        except Exception as e:
            # Table may not exist yet — fall back gracefully
            self.cbam_defaults_cache = {}
            self.cbam_defaults_count = 0
            self.cbam_defaults_load_error = str(e)

    def _lookup_cbam_default(self, cn_code: str, origin_country: str, year: int):
        """
        Look up the Commission's default emission factor from the cbam_defaults table.
        
        Tries progressively shorter CN prefixes (e.g. 72085100 → 720851 → 7208 → 72)
        to find the most specific match. Tries country-specific first, then global.
        
        Returns (effective_value, includes_indirect, source_label, match_level) or (None, None, None, None).
        """
        if not self.cbam_defaults_cache or not cn_code:
            return None, None, None, None
        
        clean_cn = re.sub(r"\D", "", cn_code)
        country_lower = origin_country.lower().strip() if origin_country else None
        
        # Try progressively shorter CN prefixes
        prefixes = []
        for length in range(len(clean_cn), 1, -1):
            prefixes.append(clean_cn[:length])
        
        for prefix in prefixes:
            match_digits = len(prefix)
            label = "COMMISSION_DEFAULT" if match_digits >= 8 else f"COMMISSION_DEFAULT_APPROX_{match_digits}D"
            # Try country-specific first
            if country_lower:
                key = (prefix, year, country_lower)
                if key in self.cbam_defaults_cache:
                    d = self.cbam_defaults_cache[key]
                    return d.effective_value, d.includes_indirect, label, match_digits
            # Then try global default (origin_country = NULL)
            key = (prefix, year, None)
            if key in self.cbam_defaults_cache:
                d = self.cbam_defaults_cache[key]
                return d.effective_value, d.includes_indirect, label, match_digits
        
        return None, None, None, None

    def _get_best_match(self, raw_name: str, allowed_cats_tuple: tuple | None):
        """Robust fuzzy matcher: top-5 candidates with stainless/SS304/inox guard. Per-instance cached."""
        cache_key = (raw_name, allowed_cats_tuple)
        if cache_key in self._match_cache:
            return self._match_cache[cache_key]
        
        # Cap the cache size for memory safety in long-running processes
        if len(self._match_cache) > 5000:
            self._match_cache.clear()
        
        candidates = self.mat_names
        if allowed_cats_tuple is not None:
            if not allowed_cats_tuple:
                candidates = []
            else:
                candidates = []
                for cat in allowed_cats_tuple:
                    candidates.extend(self.cat_to_names.get(cat, []))
        if not candidates:
            self._match_cache[cache_key] = None
            return None
        
        matches = process.extract(raw_name, candidates, scorer=fuzz.token_sort_ratio, limit=5)
        
        q_lower = raw_name.lower()
        stainless_aliases = {"stainless", "ss304", "ss316", "ss201", "inox", "304", "316", "201"}
        q_is_stainless = any(alias in q_lower for alias in stainless_aliases)
        
        for m in matches:
            m_name, m_score = m[0], m[1]
            if m_score < 75:
                continue
                
            # Guard: Don't mismatch stainless vs non-stainless (either direction)
            m_lower = m_name.lower()
            m_is_stainless = any(alias in m_lower for alias in stainless_aliases)
            if q_is_stainless != m_is_stainless:
                continue
                
            self._match_cache[cache_key] = m
            return m
        self._match_cache[cache_key] = None
        return None

    def process_bom(self, df, material_col, weight_col, strict_mode=True, disable_deminimis=False):
        # Auto-detect column mappings if the explicit ones are missing
        actual_mat_col = material_col
        if material_col not in df.columns:
            # Prioritize 'name' or 'desc' columns, explicit exclude 'id'
            for guess in ["name", "material", "part", "component", "grade", "description", "item"]:
                matches = [c for c in df.columns if guess in str(c).lower() and "id" not in str(c).lower()]
                if matches:
                    actual_mat_col = matches[0]
                    break
                    
        actual_weight_col = weight_col
        if weight_col not in df.columns:
            for guess in ["weight", "qty", "quantity", "mass", "amount"]:
                matches = [c for c in df.columns if guess in str(c).lower()]
                if matches:
                    actual_weight_col = matches[0]
                    break
        
        # Determine multiplier if weight is in tonnes
        weight_multiplier = 1.0
        if actual_weight_col in df.columns and ("tonne" in str(actual_weight_col).lower() or "ton" in str(actual_weight_col).lower()):
            weight_multiplier = 1000.0

        enriched_rows = []
        seen_ids = set()
        
        # Convert to list of dicts for orders-of-magnitude faster iteration than iterrows()
        records = df.to_dict(orient='records')
        
        for i, row in enumerate(records):
            if i > 0 and i % 5000 == 0:
                print(f"Processed {i} rows...", flush=True)
            errors = []
            quarantine_reasons = []
            notes = []
            
            def extract_string(aliases):
                invalid_vals = {"nan", "n/a", "none", "null", "-", ""}
                # Pass 1: exact column name match (highest priority)
                for k in row.keys():
                    k_lower = str(k).lower().strip()
                    if any(a == k_lower for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower().strip() not in invalid_vals:
                            return str(val).strip()
                        return None  # Exact match found but value is blank
                # Pass 2: prefix/suffix boundary match (e.g. 'id' matches 'material_id')
                for k in row.keys():
                    k_lower = str(k).lower().strip()
                    if any(k_lower.startswith(a + '_') or k_lower.endswith('_' + a) for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower().strip() not in invalid_vals:
                            return str(val).strip()
                return None
            
            mat_id = extract_string(['material_id', 'id', 'item_no', 'part_number'])
            if not mat_id:
                errors.append("Missing material ID")
                quarantine_reasons.append("Missing material ID")
            else:
                mat_id_lower = str(mat_id).strip().lower()
                if mat_id_lower in seen_ids:
                    quarantine_reasons.append("Duplicate material ID")
                else:
                    seen_ids.add(mat_id_lower)

            val_name = row.get(actual_mat_col)
            if pd.notna(val_name) and str(val_name).strip() != "" and str(val_name).lower() != "nan":
                raw_name = str(val_name).strip()
            else:
                raw_name = ""
                errors.append("Missing material name")
                quarantine_reasons.append("Missing material name")
            raw_weight = row.get(actual_weight_col, None)
            if pd.isna(raw_weight) or str(raw_weight).strip() == "" or str(raw_weight).lower() == "nan":
                errors.append("Missing quantity")
                quarantine_reasons.append("Missing quantity")
                weight_kg = 0.0
            else:
                try:
                    import math
                    if isinstance(raw_weight, str):
                        raw_weight = str(raw_weight).replace(',', '')
                    weight_kg = float(raw_weight) * weight_multiplier
                    if math.isinf(weight_kg) or math.isnan(weight_kg):
                        raise ValueError("Infinity or NaN")
                    if weight_kg < 0:
                        quarantine_reasons.append("Negative quantity")
                        weight_kg = 0.0
                    elif weight_kg > 100_000_000:
                        quarantine_reasons.append("Quantity exceeds 100M kg limit")
                except ValueError:
                    errors.append("Non-numeric quantity")
                    quarantine_reasons.append("Non-numeric quantity")
                    weight_kg = 0.0
                
            if not raw_name or str(raw_name).strip() == "" or str(raw_name).lower() == "nan":
                errors.append("Missing material name")
                raw_name = "UNKNOWN" 
                
            def extract_float(aliases, field_name):
                for k in row.keys():
                    if any(a in str(k).lower() for a in aliases):
                        val = row[k]
                        if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
                            if field_name: errors.append(f"Missing {field_name}")
                            return None
                        try:
                            if isinstance(val, str):
                                val = str(val).replace('€', '').replace('$', '').strip()
                                if ',' in val and '.' not in val:
                                    parts = val.split(',')
                                    if len(parts[-1]) == 3:
                                        val = val.replace(',', '')
                                    else:
                                        val = val.replace(',', '.')
                                elif ',' in val and '.' in val:
                                    val = val.replace(',', '')
                            fval = float(val)
                            import math
                            if math.isinf(fval) or math.isnan(fval):
                                raise ValueError("Infinity or NaN")
                            return fval
                        except ValueError:
                            if field_name: errors.append(f"Non-numeric {field_name}")
                            return None
                return None

            direct_em = extract_float(['direct_emissions', 'direct emissions'], 'direct emissions')
            if direct_em is not None and direct_em < 0:
                errors.append("Direct emissions cannot be negative")
                direct_em = 0.0

            indirect_em = extract_float(['indirect_emissions', 'indirect emissions'], None)
            if indirect_em is not None and indirect_em < 0:
                errors.append("Indirect emissions cannot be negative")
                indirect_em = 0.0
                
            price_paid_val = extract_float(['carbon_price_paid', 'price_paid', 'domestic_carbon'], None)
            price_paid = price_paid_val or 0.0
            if price_paid < 0:
                errors.append("Carbon price cannot be negative")
                price_paid = 0.0
            
            supplier_name = extract_string(['supplier_name', 'supplier', 'vendor'])
            if not supplier_name:
                errors.append("Missing supplier name")

            supplier_risk = extract_float(['supplier_risk', 'vendor_risk'], 'supplier risk') or 0.0
            if supplier_risk > 100:
                errors.append("Risk score capped at 100")
                supplier_risk = 100.0
            if supplier_risk < 0:
                errors.append("Risk score must be positive")
                supplier_risk = 0.0
                
            lead_time = extract_float(['lead_time', 'lead time'], None)
            if lead_time is None:
                errors.append("Missing lead time")
            elif lead_time < 0 or lead_time > 3650:
                errors.append("Lead time out of plausible bounds")

            single_source = extract_string(['single_source', 'sole_source'])
            if not single_source:
                errors.append("Missing single_source_flag")
            elif single_source.lower() not in ('yes', 'no', 'true', 'false', 'y', 'n'):
                errors.append("Invalid single_source_flag")
                
            geo_risk = extract_string(['geopolitical', 'geo_risk', 'country_risk'])
            if not geo_risk:
                errors.append("Missing geopolitical_risk")
            elif geo_risk.lower() not in ('low', 'medium', 'high'):
                errors.append("Invalid geopolitical_risk")
                
            data_quality = extract_string(['data_quality', 'data quality'])
            if not data_quality:
                errors.append("Missing data quality")
            else:
                dq_lower = data_quality.lower()
                if not any(x in dq_lower for x in ['verified', 'default', 'estimated', 'measured']):
                    errors.append("Invalid data quality")
                elif 'verified' in dq_lower and price_paid_val is None:
                    errors.append("Missing carbon price for Verified data")
                
            cn_code = extract_string(['cn_code', 'hs_code', 'cn code'])
            clean_cn = ""
            if not cn_code:
                errors.append("Missing CN Code")
            else:
                # Normalise once: strip all non-digits (handles "7208.51.00", "7208 51 00", 72085100.0)
                clean_cn = re.sub(r"\D", "", str(cn_code))
                if len(clean_cn) < 4 or not clean_cn.isdigit():
                    errors.append("Invalid CN Code format")
                    quarantine_reasons.append("Invalid CN Code format")
                
            def extract_exact_string(aliases):
                invalid_vals = {"nan", "n/a", "none", "null", "-", ""}
                for k in row.keys():
                    if any(a == str(k).lower().strip() for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower().strip() not in invalid_vals:
                            return str(val).strip()
                return None

            def clean_country(c):
                c = c.lower().strip()
                return self.COUNTRY_ALIASES.get(c, c)
                
            country = extract_exact_string(['country_of_origin', 'supplier_country', 'origin', 'country'])
            if not country:
                errors.append("Missing supplier country")
                quarantine_reasons.append("Missing origin country")
            else:
                c_lower = clean_country(country)
                invalid_countries = ['nowhereland', 'atlantis', 'narnia', 'test', 'unknown']
                if len(c_lower) < 2 or c_lower in invalid_countries:
                    errors.append("Unrecognized country")
                    quarantine_reasons.append("Unrecognized origin country")
                if c_lower in self.EU_EEA_COUNTRIES:
                    notes.append("Origin is exempt from CBAM (EU/EEA)")
                    
            destination = extract_exact_string(['destination', 'destination_country'])
            if not destination:
                errors.append("Missing destination country")
                quarantine_reasons.append("Missing destination country")
            else:
                d_lower = clean_country(destination)
                invalid_countries = ['nowhereland', 'atlantis', 'narnia', 'test', 'unknown']
                if len(d_lower) < 2 or d_lower in invalid_countries:
                    errors.append("Unrecognized destination country")
                    quarantine_reasons.append("Unrecognized destination country")
                elif d_lower not in self.EU_DESTINATION_COUNTRIES:
                    notes.append("Destination outside EU (exempt)")
                    
            release_date = extract_string(['release_for_free_circulation_date', 'release_date'])
            is_fallback_date = False
            if not release_date:
                release_date = extract_string(['last_shipment_date', 'shipment_date', 'date'])
                if release_date:
                    is_fallback_date = True
                    
            if not release_date:
                errors.append("Missing release/shipment date")
                quarantine_reasons.append("Missing date")
            else:
                if is_fallback_date:
                    notes.append("Using shipment date as fallback. Year grouping should ideally use release-for-free-circulation date.")
                try:
                    dt = datetime.datetime.strptime(release_date, "%Y-%m-%d")
                    if dt > datetime.datetime.now():
                        errors.append("Date cannot be in the future")
                        quarantine_reasons.append("Date cannot be in the future")
                    elif dt < datetime.datetime(2026, 1, 1):
                        notes.append("Pre-2026 release (reporting-only phase, no financial liability)")
                except ValueError:
                    errors.append("Invalid date format (requires YYYY-MM-DD)")
                    quarantine_reasons.append("Invalid date format")
            
            # ── Sector determination: CN code is the source of truth ──
            cbam_sector = extract_string(['cbam_sector', 'sector'])
            
            sector_valid = False
            sector_lower = ""
            allowed_cats = None
            is_out_of_scope = False
            
            cn_status, cn_derived_sector = self.get_sector_from_cn(clean_cn) if clean_cn else ("NOT_COVERED", None)
            
            invalid_sector_vals = {"nan", "n/a", "none", "null", "-", ""}
            declared_sector = None
            if cbam_sector and cbam_sector.strip().lower() not in invalid_sector_vals:
                declared_sector = cbam_sector.strip().lower()
            
            missing_scope_msg = None
            if cn_status == "EXACT_MATCH":
                sector_lower = cn_derived_sector
                sector_valid = True
                for keyword, cats in self.CBAM_SECTOR_CATEGORY_MAP.items():
                    if keyword in sector_lower:
                        allowed_cats = cats
                        break
                if declared_sector and declared_sector != sector_lower:
                    if not any(k in declared_sector for k in sector_lower.split()):
                        errors.append(f"Declared sector '{declared_sector}' differs from CN-derived sector '{sector_lower}'")
            elif cn_status == "INCOMPLETE":
                errors.append("Incomplete CN code (need 8-digit EU CN)")
                quarantine_reasons.append("Incomplete CN code, needs 8-digit EU CN")
            elif cn_status == "EXCLUDED":
                is_out_of_scope = True
                notes.append("CN code is explicitly excluded from CBAM Annex I (e.g., scrap/waste)")
            elif declared_sector:
                # cn_status == "NOT_COVERED", but user declared a sector
                for keyword, cats in self.CBAM_SECTOR_CATEGORY_MAP.items():
                    if keyword == declared_sector or keyword in declared_sector:
                        allowed_cats = cats
                        sector_lower = declared_sector
                        break
                if allowed_cats is not None or sector_lower:
                    errors.append(f"CN code '{clean_cn}' not found in Annex I for declared sector '{declared_sector}'")
                    quarantine_reasons.append("CN code not found in Annex I for declared sector")
                else:
                    is_out_of_scope = True
                    notes.append(f"Sector '{declared_sector}' is not covered by CBAM")
            else:
                missing_scope_msg = "Cannot determine CBAM scope"
                if clean_cn:
                    errors.append("CN code not in CBAM Annex I")
                    missing_scope_msg = "CN code not in CBAM Annex I"
                else:
                    errors.append("Both sector and CN code missing")
                    missing_scope_msg = "Both sector and CN code missing"
                quarantine_reasons.append(missing_scope_msg)

            match_tuple = self._get_best_match(raw_name, tuple(allowed_cats) if allowed_cats else None)
            is_match = match_tuple is not None
            
            # If quarantined due to missing scope, but we matched a Polymer, soften to OUT OF SCOPE.
            # GUARD: Only fire when there's NO in-scope CN code AND no recognised CBAM sector.
            # A "plastic-coated steel pipe" with CN 7306 must stay in scope because CN evidence wins.
            if missing_scope_msg and not sector_valid and not is_out_of_scope and not cn_derived_sector and missing_scope_msg in quarantine_reasons:
                if is_match:
                    mat_obj = self.mat_dict.get(match_tuple[0])
                    mat_cat = mat_obj.category if mat_obj else None
                    if mat_cat and "polymer" in mat_cat.lower():
                        quarantine_reasons.remove(missing_scope_msg)
                        if missing_scope_msg in errors: errors.remove(missing_scope_msg)
                        is_out_of_scope = True
                        notes.append("Likely out of scope (matched material is a polymer, no CBAM CN code), please confirm")

            provided_carbon_factor = None
            # Indirect emissions: only for cement and fertilisers (CBAM definitive rules)
            # Steel and aluminium are direct emissions only
            includes_indirect = False
            if sector_lower and any(k in sector_lower for k in ['cement', 'fertili']):
                includes_indirect = True
            
            if direct_em is not None and direct_em > 50.0:
                quarantine_reasons.append("Emissions exceed plausibility bound (50 t/t)")
                
            if includes_indirect and indirect_em is not None and indirect_em > 50.0:
                quarantine_reasons.append("Emissions exceed plausibility bound (50 t/t)")
            
            if direct_em is not None:
                provided_carbon_factor = direct_em
                if includes_indirect:
                    if indirect_em is not None:
                        provided_carbon_factor += indirect_em
                    else:
                        errors.append("Missing indirect emissions (using fallback default for total)")
                        provided_carbon_factor = None # Invalidate so it uses full db/fallback factor
                elif not includes_indirect and indirect_em is not None:
                    notes.append("Indirect emissions excluded for this sector (CBAM definitive rules)")
            
            emissions_basis = "SUPPLIED"
            
            # Determine the lookup year from release date (default to current year)
            lookup_year = datetime.datetime.now().year
            if release_date:
                try:
                    dt_ship = datetime.datetime.strptime(release_date, "%Y-%m-%d")
                    lookup_year = dt_ship.year
                    if lookup_year < 2026:
                        lookup_year = 2026  # Use 2026 defaults for pre-2026 dates
                    # Warn near year boundary: Dec shipments may arrive in Jan (different calendar year)
                    if dt_ship.month == 12 and dt_ship.day >= 15:
                        notes.append(f"Year boundary warning: Dec shipment may be released for free circulation in {lookup_year + 1}. De minimis year could differ.")
                except (ValueError, IndexError):
                    pass
            
            # Extract origin country for DB lookup
            origin_country_raw = extract_string(['country_of_origin', 'origin_country', 'supplier_country', 'country'])
            
            if is_match:
                matched_name = match_tuple[0]
                confidence = match_tuple[1]
                mat = self.mat_dict.get(matched_name)
                db_carbon = mat.embodied_carbon if (mat and mat.embodied_carbon) else 0.0
                
                if provided_carbon_factor is not None:
                    carbon_factor = provided_carbon_factor
                else:
                    # Try DB-backed Commission defaults first (by CN code + country + year)
                    db_default, db_incl_indirect, db_source, match_level = self._lookup_cbam_default(
                        cn_code or "", origin_country_raw or "", lookup_year
                    )
                    if db_default is not None:
                        carbon_factor = db_default
                        emissions_basis = db_source
                        if self.cbam_defaults_stale:
                            notes.append("CBAM default values may be outdated (>90 days since last refresh)")
                        if match_level and match_level < 8:
                            notes.append(f"Using approximate {match_level}-digit CN default (exact 8-digit match not found)")
                    elif db_carbon > 0:
                        carbon_factor = db_carbon
                        emissions_basis = "DEFAULT_FALLBACK"
                    else:
                        carbon_factor = _estimate_carbon_factor(mat.name, mat.category)
                        emissions_basis = "GENERIC_ESTIMATE"
                        if sector_valid:
                            errors.append("No Commission default found; using generic ICE-derived estimate (not suitable for compliance)")
                            quarantine_reasons.append("In-scope row using generic estimate, not a Commission default")
                obsolete_flag = "YES" if (mat and mat.is_obsolete) else "NO"
                replacement = mat.replacement_standard if (mat and mat.replacement_standard) else "N/A"
                recyclability = mat.recyclability_index if (mat and mat.recyclability_index) else 0.5
            else:
                matched_name = "NO MATCH FOUND"
                confidence = 0
                if provided_carbon_factor is not None:
                    carbon_factor = provided_carbon_factor
                else:
                    # Try DB-backed Commission defaults first
                    db_default, db_incl_indirect, db_source, match_level = self._lookup_cbam_default(
                        cn_code or "", origin_country_raw or "", lookup_year
                    )
                    if db_default is not None:
                        carbon_factor = db_default
                        emissions_basis = db_source
                        if self.cbam_defaults_stale:
                            notes.append("CBAM default values may be outdated (>90 days since last refresh)")
                        if match_level and match_level < 8:
                            notes.append(f"Using approximate {match_level}-digit CN default (exact 8-digit match not found)")
                    else:
                        carbon_factor = _estimate_carbon_factor(raw_name, "")
                        emissions_basis = "GENERIC_ESTIMATE"
                        if sector_valid:
                            errors.append("No Commission default found; using generic ICE-derived estimate (not suitable for compliance)")
                            quarantine_reasons.append("In-scope row using generic estimate, not a Commission default")
                obsolete_flag = "N/A"
                replacement = "N/A"
                recyclability = 0.5
                
            # Apply regulatory mark-ups if using Commission Defaults (e.g. 1% for fertilisers, 20% for others)
            # This penalises importers who don't use actual verified emissions.
            if emissions_basis == "COMMISSION_DEFAULT":
                markup = 1.01 if sector_lower == "fertiliser" else 1.20
                carbon_factor = carbon_factor * markup
                notes.append(f"Applied {int(round((markup-1)*100))}% regulatory mark-up for using default values")

            total_co2_kg = round(weight_kg * carbon_factor, 3)
            total_co2_tonnes = total_co2_kg / 1000.0
            
            net_cbam_price = max(CBAM_REFERENCE_PRICE_EUR - price_paid, 0.0)
            if price_paid > 0 and net_cbam_price == 0:
                notes.append(f"Full carbon price already paid at origin ({price_paid} EUR/t)")
            elif price_paid > 0:
                notes.append(f"Partial carbon price paid at origin ({price_paid} EUR/t); net price {net_cbam_price} EUR/t")
            
            is_exempt = False
            if "Origin is exempt from CBAM (EU/EEA)" in notes or "Destination outside EU (exempt)" in notes or "Pre-2026 shipment (reporting-only phase, no financial liability)" in notes:
                is_exempt = True
            
            cbam_cost_eur = total_co2_tonnes * net_cbam_price if sector_valid and not is_exempt else 0.0
            
            # Apply Free Allocation Phase-Out (Phase-in of CBAM costs)
            if cbam_cost_eur > 0 and lookup_year >= 2026:
                phase_in_schedule = {
                    2026: 0.025, 2027: 0.05, 2028: 0.10, 2029: 0.225, 
                    2030: 0.485, 2031: 0.61, 2032: 0.735, 2033: 0.86, 2034: 1.0
                }
                phase_in = phase_in_schedule.get(lookup_year, 1.0)
                cbam_cost_eur = cbam_cost_eur * phase_in
                if phase_in < 1.0:
                    notes.append(f"Cost adjusted by {phase_in*100:.1f}% free allocation phase-out for {lookup_year}")
                    
            cbam_cost_eur = round(cbam_cost_eur, 2)
            
            carbon_score = min(carbon_factor / 30.0 * 50, 50)
            if geo_risk or single_source or supplier_risk > 0:
                geo_score = 15 if geo_risk and "high" in geo_risk.lower() else (7.5 if geo_risk and "med" in geo_risk.lower() else 0)
                ss_score = 15 if single_source and ("yes" in single_source.lower() or "true" in single_source.lower() or "y" == single_source.lower()) else 0
                supp_score = min(supplier_risk / 100.0 * 20, 20)
                lead_score = 10 if lead_time and lead_time > 180 else (5 if lead_time and lead_time > 90 else 0)
                dq_score = 0
                if data_quality:
                    if 'default' in data_quality.lower() or 'unknown' in data_quality.lower():
                        dq_score = 10
                    elif 'estimated' in data_quality.lower():
                        dq_score = 5
                base_esg = carbon_score + geo_score + ss_score + supp_score + lead_score + dq_score
            else:
                recycle_score = (1 - recyclability) * 30
                obsolete_score = 20 if obsolete_flag == "YES" else 0
                base_esg = carbon_score + recycle_score + obsolete_score
            esg_risk = round(min(base_esg, 100), 1)

            raw_total_co2_kg = total_co2_kg
            raw_total_co2_tonnes = total_co2_tonnes
            raw_cbam_cost_eur = cbam_cost_eur
            
            if strict_mode:
                cbam_critical_errors = [
                    "Missing material ID", "Missing material name", "Missing quantity", "Non-numeric quantity",
                    "Missing CN Code", "Invalid CN Code format", "Missing supplier country",
                    "Unrecognized country", "Missing destination country", "Unrecognized destination country",
                    "Missing shipment date", "Shipment date cannot be in the future", "Invalid date format"
                ]
                for err in errors:
                    if err not in quarantine_reasons and any(err.startswith(c) for c in cbam_critical_errors):
                        quarantine_reasons.append(f"Strict Mode: {err}")
            
            if quarantine_reasons:
                included_str = "QUARANTINED: " + " | ".join(quarantine_reasons)
                total_co2_kg = 0.0
                total_co2_tonnes = 0.0
                cbam_cost_eur = 0.0
                esg_risk = 0.0
            elif is_out_of_scope:
                included_str = "OUT OF SCOPE"
                total_co2_kg = 0.0
                total_co2_tonnes = 0.0
                cbam_cost_eur = 0.0
                # ESG risk is still calculated for out of scope
            else:
                included_str = "YES"

            clean_row = {}
            for k, v in row.items():
                if isinstance(v, str) and str(v).startswith(('=', '+', '-', '@')):
                    clean_row[k] = f"'{v}"
                else:
                    clean_row[k] = v

            
            is_deminimis_eligible = "NO"
            if cn_status == "EXACT_MATCH" and sector_lower:
                if any(x in sector_lower for x in ['electric', 'hydrogen']):
                    notes.append(f"De minimis exemption does not apply to {sector_lower.title()}")
                elif "Origin is exempt" not in " | ".join(notes) and "Destination outside EU" not in " | ".join(notes):
                    is_deminimis_eligible = "YES"

            raw_importer = extract_string(['importer', 'eori', 'importer_id', 'importer_name'])
            importer = raw_importer.strip().upper() if raw_importer else "UNKNOWN_IMPORTER"
            
            other_imports_t = 0.0
            other_imports_str = extract_string(['other_cbam_imports_this_year_t', 'other_cbam_imports_t', 'other_imports_t'])
            if other_imports_str:
                try:
                    other_imports_t = float(other_imports_str.replace(',', ''))
                except ValueError:
                    pass
                
            enriched_rows.append({
                **clean_row,
                "Parsed_Weight_kg": round(weight_kg, 2),
                "Importer": importer,
                "Other_Imports_t": other_imports_t,
                "Lookup_Year": lookup_year,
                "DeMinimis_Eligible_Mass_kg": weight_kg if is_deminimis_eligible == "YES" else 0.0,
                "Matched_Material": matched_name,
                "Match_Confidence": f"{confidence}%" if is_match else "0%",
                "Carbon_Factor_kgCO2e_per_kg": round(carbon_factor, 3),
                "Emissions_Basis": emissions_basis,
                "Total_CO2_kg": round(total_co2_kg, 3) if total_co2_kg > 0 else 0.0,
                "Total_CO2_tonnes": round(total_co2_tonnes, 4) if total_co2_tonnes > 0 else 0.0,
                "CBAM_Cost_EUR": cbam_cost_eur if cbam_cost_eur > 0 else 0.0,
                "Provisional_CO2_kg": round(raw_total_co2_kg, 3),
                "Provisional_CO2_tonnes": round(raw_total_co2_tonnes, 4),
                "Provisional_CBAM_Cost_EUR": round(raw_cbam_cost_eur, 2),
                "Domestic_Carbon_Price_Paid_EUR": price_paid,
                "Net_CBAM_Price_EUR": net_cbam_price,
                "Is_Obsolete": obsolete_flag,
                "Replacement_Standard": replacement,
                "ESG_Risk_Score": esg_risk if esg_risk > 0 else 0.0,
                "Notes": " | ".join(notes) if notes else "None",
                "Validation_Errors": " | ".join(list(dict.fromkeys(errors + quarantine_reasons))) if (errors or quarantine_reasons) else "None",
                "Included_In_Total": included_str,
                "CBAM_Estimate_Notice": "Estimate only - not a CBAM declaration"
            })

        # Group by Importer and Calendar Year for De Minimis (use integer grams for precision)
        grams_by_importer_year = defaultdict(int)
        other_imports_by_group = {}
        other_imports_conflict = set()
        
        for r in enriched_rows:
            key = (r["Importer"], r["Lookup_Year"])
            mass_kg = r.get("DeMinimis_Eligible_Mass_kg", 0.0)
            if mass_kg > 0:
                grams_by_importer_year[key] += int(round(mass_kg * 1000))
                
            # Track other imports
            other_t = r.get("Other_Imports_t", 0.0)
            other_g = int(round(other_t * 1000000))
            if other_g > 0:
                if key in other_imports_by_group and other_imports_by_group[key] != other_g:
                    other_imports_conflict.add(key)
                    other_imports_by_group[key] = max(other_imports_by_group[key], other_g)
                else:
                    other_imports_by_group[key] = other_g
        
        for r in enriched_rows:
            r["CBAM_Cost_If_Not_Exempt_EUR"] = r.get("CBAM_Cost_EUR", 0.0)
            if disable_deminimis:
                r["DeMinimis_Status"] = "Disabled by user"
            elif r.get("DeMinimis_Eligible_Mass_kg", 0.0) > 0:
                key = (r["Importer"], r["Lookup_Year"])
                total_grams = grams_by_importer_year[key]
                other_imports_grams = other_imports_by_group.get(key, 0)
                grand_total_grams = total_grams + other_imports_grams
                
                headroom_grams = max(50000000 - grand_total_grams, 0)
                headroom_t = headroom_grams / 1000000.0
                
                importer_label = r["Importer"]
                if importer_label == "UNKNOWN_IMPORTER":
                    importer_label = "importer unknown, grouped together"
                    
                conflict_warn = ""
                if key in other_imports_conflict:
                    conflict_warn = f"WARNING: Conflicting 'other_imports' values for {importer_label}. Using highest ({other_imports_grams/1000000:.1f}t). | "
                
                # Build the breakdown note
                breakdown_note = f"{conflict_warn}De minimis tally ({importer_label} in {r['Lookup_Year']}): {total_grams/1000000:.1f}t in file, {other_imports_grams/1000000:.1f}t other."
                current_notes = r.get("Notes", "None")
                if current_notes == "None":
                    r["Notes"] = breakdown_note
                elif "De minimis tally" not in current_notes:
                    r["Notes"] = current_notes + " | " + breakdown_note

                # Allow strictly <= 50,000,000 grams (exactly 50t is exempt)
                if grand_total_grams <= 50000000:
                    r["DeMinimis_Status"] = f"Possibly exempt (headroom: {headroom_t:.1f}t, verify annual total <= 50t)"
                    if headroom_t <= 5.0:
                        r["Notes"] = r["Notes"] + " | WARNING: Very close to 50t threshold"
                else:
                    r["DeMinimis_Status"] = "Not exempt (Once >50t, all embedded emissions for the year are in scope)"
            else:
                r["DeMinimis_Status"] = "N/A"
        
        # Add diagnostics to every row for CSV/PDF traceability
        annex_version = "Regulation (EU) 2023/956 Annex I"
        defaults_info = f"CBAM rules: {annex_version} | Defaults loaded: {self.cbam_defaults_count} entries"
        if self.cbam_defaults_version:
            defaults_info += f", version: {self.cbam_defaults_version}"
        if self.cbam_defaults_load_error:
            defaults_info += f", LOAD ERROR: {self.cbam_defaults_load_error}"
        if self.cbam_defaults_count == 0:
            defaults_info += " | WARNING: No Commission defaults loaded — all factors are estimates"
        for r in enriched_rows:
            r["CBAM_Defaults_Info"] = defaults_info

        return pd.DataFrame(enriched_rows)
