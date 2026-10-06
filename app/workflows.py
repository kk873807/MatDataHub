import pandas as pd
import math
import datetime
from thefuzz import process, fuzz
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

    def __init__(self, db: Session):
        self.db = db
        all_mats = self.db.query(Material.id, Material.name, Material.category).all()
        self.mat_dict = {m.id: m.name for m in all_mats}
        # Filter out names shorter than MIN_CANDIDATE_LENGTH
        self.mat_names = [m.name for m in all_mats if len(m.name) >= self.MIN_CANDIDATE_LENGTH]
        # Build category → [name, ...] for sector-aware pre-filtering
        self.cat_to_names = {}
        for m in all_mats:
            if len(m.name) >= self.MIN_CANDIDATE_LENGTH:
                cat = (m.category or "").strip()
                self.cat_to_names.setdefault(cat, []).append(m.name)
        
        # Preload CBAM defaults into memory for fast lookups
        self.cbam_defaults_cache = {}
        self.cbam_defaults_stale = False
        try:
            all_defaults = self.db.query(CBAMDefault).all()
            for d in all_defaults:
                key = (d.cn_prefix, d.year, (d.origin_country or "").lower() if d.origin_country else None)
                self.cbam_defaults_cache[key] = d
            if all_defaults:
                latest = max(d.updated_at for d in all_defaults if d.updated_at)
                if latest and (datetime.datetime.now(latest.tzinfo) - latest).days > 90:
                    self.cbam_defaults_stale = True
        except Exception:
            # Table may not exist yet — fall back gracefully
            self.cbam_defaults_cache = {}

    def _lookup_cbam_default(self, cn_code: str, origin_country: str, year: int):
        """
        Look up the Commission's default emission factor from the cbam_defaults table.
        
        Tries progressively shorter CN prefixes (e.g. 72085100 → 720851 → 7208 → 72)
        to find the most specific match. Tries country-specific first, then global.
        
        Returns (effective_value, includes_indirect, source_label) or (None, None, None).
        """
        if not self.cbam_defaults_cache or not cn_code:
            return None, None, None
        
        clean_cn = cn_code.replace(" ", "").replace(".", "").replace("-", "")
        country_lower = origin_country.lower().strip() if origin_country else None
        
        # Try progressively shorter CN prefixes
        prefixes = []
        for length in range(len(clean_cn), 1, -1):
            prefixes.append(clean_cn[:length])
        
        for prefix in prefixes:
            # Try country-specific first
            if country_lower:
                key = (prefix, year, country_lower)
                if key in self.cbam_defaults_cache:
                    d = self.cbam_defaults_cache[key]
                    return d.effective_value, d.includes_indirect, "COMMISSION_DEFAULT"
            # Then try global default (origin_country = NULL)
            key = (prefix, year, None)
            if key in self.cbam_defaults_cache:
                d = self.cbam_defaults_cache[key]
                return d.effective_value, d.includes_indirect, "COMMISSION_DEFAULT"
        
        return None, None, None

    def process_bom(self, df, material_col, weight_col, strict_mode=False):
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
        for index, row in df.iterrows():
            errors = []
            quarantine_reasons = []
            notes = []
            
            def extract_string(aliases):
                # Pass 1: exact column name match (highest priority)
                for k in row.keys():
                    k_lower = str(k).lower().strip()
                    if any(a == k_lower for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                            return str(val).strip()
                        return None  # Exact match found but value is blank
                # Pass 2: prefix/suffix boundary match (e.g. 'id' matches 'material_id')
                for k in row.keys():
                    k_lower = str(k).lower().strip()
                    if any(k_lower.startswith(a + '_') or k_lower.endswith('_' + a) for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
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

            raw_name = str(row.get(actual_mat_col, ""))
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
                clean_cn = cn_code.replace(" ", "").replace(".", "").replace("-", "")
                if not clean_cn.isdigit() or len(clean_cn) < 4:
                    errors.append("Invalid CN Code format")
                    quarantine_reasons.append("Invalid CN Code format")
                
            def extract_exact_string(aliases):
                for k in row.keys():
                    if any(a == str(k).lower().strip() for a in aliases):
                        val = row[k]
                        if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                            return str(val).strip()
                return None

            def clean_country(c):
                c = c.lower().strip()
                if c == 'the netherlands': return 'netherlands'
                if c == 'usa' or c == 'united states of america': return 'united states'
                if c == 'uk' or c == 'great britain': return 'united kingdom'
                return c
                
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
                    
            shipment_date = extract_string(['last_shipment_date', 'shipment_date', 'date'])
            if not shipment_date:
                errors.append("Missing shipment date")
                quarantine_reasons.append("Missing shipment date")
            else:
                try:
                    dt = datetime.datetime.strptime(shipment_date, "%Y-%m-%d")
                    if dt > datetime.datetime.now():
                        errors.append("Shipment date cannot be in the future")
                        quarantine_reasons.append("Shipment date cannot be in the future")
                    elif dt < datetime.datetime(2026, 1, 1):
                        notes.append("Pre-2026 shipment (reporting-only phase, no financial liability)")
                except ValueError:
                    errors.append("Invalid date format (requires YYYY-MM-DD)")
                    quarantine_reasons.append("Invalid date format")
            
            cbam_sector = extract_string(['cbam_sector', 'sector'])
            candidates = self.mat_names

            sector_valid = False
            sector_lower = ""
            allowed_cats = None
            if cbam_sector and cbam_sector.lower() not in ('nan', ''):
                sector_lower = cbam_sector.strip().lower()
                for keyword, cats in self.CBAM_SECTOR_CATEGORY_MAP.items():
                    if keyword in sector_lower:
                        allowed_cats = cats
                        break
                
                if allowed_cats is None:
                    quarantine_reasons.append("Sector not covered by CBAM")
                    errors.append("Sector not covered by CBAM")
                else:
                    sector_valid = True
                    if allowed_cats:
                        candidates = []
                        for cat in allowed_cats:
                            candidates.extend(self.cat_to_names.get(cat, []))
                    elif allowed_cats == []:
                        candidates = []
            else:
                # No sector provided. See if CN code can rescue it, otherwise quarantine.
                if not cn_code or not any(cn_code.replace(" ", "").startswith(p) for p in ['72','73','2523','76','31','2814','2804']):
                    quarantine_reasons.append("Sector missing and CN code not covered by CBAM")
                    errors.append("Sector missing and CN code not covered by CBAM")
                else:
                    # Guessed valid via CN code
                    sector_valid = True

            match_tuple = process.extractOne(
                raw_name, candidates, scorer=fuzz.token_sort_ratio
            ) if candidates else None
            is_match = match_tuple and match_tuple[1] > 60

            provided_carbon_factor = None
            includes_indirect = False
            if allowed_cats is not None:
                if any(k in sector_lower for k in ['cement', 'fertili']):
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

            if clean_cn and sector_lower:
                if "steel" in sector_lower or "iron" in sector_lower:
                    if not clean_cn.startswith(("72", "73", "26")):
                        errors.append("CN Code does not match Iron & Steel sector")
                        quarantine_reasons.append("CN Code does not match Iron & Steel sector")
                elif "cement" in sector_lower:
                    if not clean_cn.startswith(("2523", "2507")):
                        errors.append("CN Code does not match Cement sector")
                        quarantine_reasons.append("CN Code does not match Cement sector")
                elif "alumin" in sector_lower:
                    if not clean_cn.startswith("76"):
                        errors.append("CN Code does not match Aluminium sector")
                        quarantine_reasons.append("CN Code does not match Aluminium sector")
                elif "fertil" in sector_lower:
                    if not clean_cn.startswith(("2808", "2814", "2834", "3102", "3105")):
                        errors.append("CN Code does not match Fertilisers sector")
                        quarantine_reasons.append("CN Code does not match Fertilisers sector")

            if is_match:
                q_lower = raw_name.lower()
                m_lower = match_tuple[0].lower()
                q_is_stainless = "stainless" in q_lower
                m_is_stainless = "stainless" in m_lower
                if q_is_stainless != m_is_stainless and "steel" in q_lower:
                    is_match = False
            
            emissions_basis = "SUPPLIED"
            
            # Determine the lookup year from shipment date (default to current year)
            lookup_year = datetime.datetime.now().year
            if shipment_date:
                try:
                    lookup_year = int(shipment_date[:4])
                    if lookup_year < 2026:
                        lookup_year = 2026  # Use 2026 defaults for pre-2026 dates
                except (ValueError, IndexError):
                    pass
            
            # Extract origin country for DB lookup
            origin_country_raw = extract_string(['country_of_origin', 'origin_country', 'supplier_country', 'country'])
            
            if is_match:
                matched_name = match_tuple[0]
                confidence = match_tuple[1]
                mat = self.db.query(Material).filter(Material.name == matched_name).first()
                db_carbon = mat.embodied_carbon if mat.embodied_carbon else 0.0
                
                if provided_carbon_factor is not None:
                    carbon_factor = provided_carbon_factor
                else:
                    # Try DB-backed Commission defaults first (by CN code + country + year)
                    db_default, db_incl_indirect, db_source = self._lookup_cbam_default(
                        cn_code or "", origin_country_raw or "", lookup_year
                    )
                    if db_default is not None:
                        carbon_factor = db_default
                        emissions_basis = "COMMISSION_DEFAULT"
                        if self.cbam_defaults_stale:
                            notes.append("CBAM default values may be outdated (>90 days since last refresh)")
                    elif db_carbon > 0:
                        carbon_factor = db_carbon
                        emissions_basis = "DEFAULT_FALLBACK"
                    else:
                        carbon_factor = _estimate_carbon_factor(mat.name, mat.category)
                        emissions_basis = "LEGACY_FALLBACK"
                obsolete_flag = "YES" if mat.is_obsolete else "NO"
                replacement = mat.replacement_standard if mat.replacement_standard else "N/A"
                recyclability = mat.recyclability_index if mat.recyclability_index else 0.5
            else:
                matched_name = "NO MATCH FOUND"
                confidence = 0
                if provided_carbon_factor is not None:
                    carbon_factor = provided_carbon_factor
                else:
                    # Try DB-backed Commission defaults first
                    db_default, db_incl_indirect, db_source = self._lookup_cbam_default(
                        cn_code or "", origin_country_raw or "", lookup_year
                    )
                    if db_default is not None:
                        carbon_factor = db_default
                        emissions_basis = "COMMISSION_DEFAULT"
                        if self.cbam_defaults_stale:
                            notes.append("CBAM default values may be outdated (>90 days since last refresh)")
                    else:
                        carbon_factor = _estimate_carbon_factor(raw_name, "")
                        emissions_basis = "LEGACY_FALLBACK"
                obsolete_flag = "N/A"
                replacement = "N/A"
                recyclability = 0.5
                
            total_co2_kg = round(weight_kg * carbon_factor, 3)
            total_co2_tonnes = total_co2_kg / 1000.0
            
            net_cbam_price = max(CBAM_REFERENCE_PRICE_EUR - price_paid, 0.0)
            
            is_exempt = False
            if "Origin is exempt from CBAM (EU/EEA)" in notes or "Destination outside EU (exempt)" in notes or "Pre-2026 shipment (reporting-only phase, no financial liability)" in notes:
                is_exempt = True
            
            cbam_cost_eur = round(total_co2_tonnes * net_cbam_price, 2) if sector_valid and not is_exempt else 0.0
            
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
                included_str = "NO: " + " | ".join(quarantine_reasons)
                total_co2_kg = 0.0
                total_co2_tonnes = 0.0
                cbam_cost_eur = 0.0
                esg_risk = 0.0
            else:
                included_str = "YES"

            clean_row = {}
            for k, v in row.to_dict().items():
                if isinstance(v, str) and str(v).startswith(('=', '+', '-', '@')):
                    clean_row[k] = f"'{v}"
                else:
                    clean_row[k] = v

            
            is_deminimis_eligible = "NO"
            if sector_valid and sector_lower and not any(x in sector_lower for x in ['electric', 'hydrogen']):
                is_deminimis_eligible = "YES"
                
            enriched_rows.append({
                **clean_row,
                "Parsed_Weight_kg": round(weight_kg, 2),
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
                "Included_In_Total": included_str
            })

        total_eligible_mass_kg = sum(r.get("DeMinimis_Eligible_Mass_kg", 0.0) for r in enriched_rows if r.get("Included_In_Total", "").startswith("YES"))
        
        if 0 < total_eligible_mass_kg <= 50000.0 and not strict_mode:
            for r in enriched_rows:
                if r.get("Included_In_Total", "").startswith("YES") and r.get("DeMinimis_Eligible_Mass_kg", 0.0) > 0:
                    r["CBAM_Cost_EUR"] = 0.0
                    current_notes = r.get("Notes", "None")
                    new_note = "De minimis exemption applies (annual eligible total <= 50t)"
                    if current_notes == "None":
                        r["Notes"] = new_note
                    else:
                        if "De minimis exemption applies" not in current_notes:
                            r["Notes"] = current_notes + " | " + new_note
        elif 0 < total_eligible_mass_kg <= 50000.0 and strict_mode:
            for r in enriched_rows:
                if r.get("Included_In_Total", "").startswith("YES") and r.get("DeMinimis_Eligible_Mass_kg", 0.0) > 0:
                    current_notes = r.get("Notes", "None")
                    new_note = "Strict Mode: De minimis exemption disabled (annual compliance unverified)"
                    if current_notes == "None":
                        r["Notes"] = new_note
                    else:
                        r["Notes"] = current_notes + " | " + new_note

        return pd.DataFrame(enriched_rows)
