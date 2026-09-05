from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/calculators", tags=["Calculators"])

# 1. Synthesizer
class SynthRequest(BaseModel):
    mat1_density: float
    mat1_tensile: float
    mat1_cost_min: float
    mat1_vol_percent: float
    mat2_density: float
    mat2_tensile: float
    mat2_cost_min: float

@router.post("/synthesizer")
def calculate_synthesizer(req: SynthRequest):
    v1 = req.mat1_vol_percent / 100.0
    v2 = 1.0 - v1
    
    blend_density = (req.mat1_density * v1) + (req.mat2_density * v2)
    blend_ts = (req.mat1_tensile * v1) + (req.mat2_tensile * v2)
    
    mass_frac1 = (req.mat1_density * v1) / blend_density if blend_density > 0 else 0
    mass_frac2 = (req.mat2_density * v2) / blend_density if blend_density > 0 else 0
    blend_cost = (req.mat1_cost_min * mass_frac1) + (req.mat2_cost_min * mass_frac2)
    
    return {
        "ok": True,
        "data": {
            "blend_density": blend_density,
            "blend_tensile": blend_ts,
            "blend_cost": blend_cost
        }
    }

# 2. Safety Factor
class SafetyRequest(BaseModel):
    yield_strength: float
    load_n: float
    area_cm2: float

@router.post("/safety_factor")
def calculate_safety(req: SafetyRequest):
    stress_mpa = req.load_n / (req.area_cm2 * 100.0)
    sf = req.yield_strength / stress_mpa if stress_mpa > 0 else float("inf")
    return {
        "ok": True,
        "data": {
            "stress_mpa": stress_mpa,
            "safety_factor": sf
        }
    }

# 3. Thermal
class ThermalRequest(BaseModel):
    material_name: str
    category: str
    part_length_mm: float
    initial_temp: float
    final_temp: float

@router.post("/thermal_expansion")
def calculate_thermal(req: ThermalRequest):
    cat = req.category.lower()
    name = req.material_name.lower()
    
    if "polymer" in cat: cte = 100.0
    elif "ceramic" in cat: cte = 5.0
    elif "semiconductor" in cat: cte = 4.0
    elif "nanomaterial" in cat: cte = 1.0
    elif "magnesium" in name: cte = 26.0
    elif "zinc" in name or "zamak" in name or "za-" in name: cte = 27.4
    elif "aluminum" in name: cte = 23.0
    elif "titanium" in name or "nitinol" in name: cte = 8.6
    elif "zirconium" in name or "zircaloy" in name: cte = 6.0
    elif "beryllium copper" in name: cte = 17.0
    elif "beryllium" in name: cte = 11.4
    else: cte = 12.0
    
    delta_t = req.final_temp - req.initial_temp
    expansion_mm = req.part_length_mm * (cte * 1e-6) * delta_t
    
    return {
        "ok": True,
        "data": {
            "cte": cte,
            "delta_t": delta_t,
            "expansion_mm": expansion_mm
        }
    }

# 4. Deflection
import math

class DeflectionRequest(BaseModel):
    material_name: str
    category: str
    elastic_modulus_gpa: Optional[float] = None
    force_n: float
    length_mm: float
    diameter_mm: float

@router.post("/beam_deflection")
def calculate_deflection(req: DeflectionRequest):
    cat = req.category.lower()
    name = req.material_name.lower()
    E_gpa = req.elastic_modulus_gpa
    
    if not E_gpa:
        if "polymer" in cat: E_gpa = 3.0
        elif "ceramic" in cat: E_gpa = 300.0
        elif "semiconductor" in cat: E_gpa = 150.0
        elif "nanomaterial" in cat: E_gpa = 1000.0
        elif "magnesium" in name: E_gpa = 45.0
        elif "zinc" in name or "zamak" in name or "za-" in name: E_gpa = 85.0
        elif "aluminum" in name: E_gpa = 69.0
        elif "titanium" in name: E_gpa = 110.0
        elif "nitinol" in name: E_gpa = 75.0
        elif "zirconium" in name or "zircaloy" in name: E_gpa = 99.0
        elif "beryllium copper" in name: E_gpa = 130.0
        elif "albemet" in name: E_gpa = 193.0
        elif "beryllium" in name: E_gpa = 303.0
        else: E_gpa = 200.0
        
    E_pa = E_gpa * 1e9
    L_m = req.length_mm / 1000.0
    d_m = req.diameter_mm / 1000.0
    
    I_m4 = (math.pi * (d_m ** 4)) / 64.0
    deflection_m = (req.force_n * (L_m ** 3)) / (3.0 * E_pa * I_m4)
    deflection_mm = deflection_m * 1000.0
    
    return {
        "ok": True,
        "data": {
            "elastic_modulus_gpa": E_gpa,
            "inertia_m4": I_m4,
            "deflection_mm": deflection_mm
        }
    }

# 5. Fatigue
class FatigueRequest(BaseModel):
    material_name: str
    category: str
    tensile_strength: float

@router.post("/fatigue_life")
def calculate_fatigue(req: FatigueRequest):
    cat = req.category.lower()
    name = req.material_name.lower()
    
    if "metal" in cat and "aluminum" not in name:
        endurance_limit = req.tensile_strength * 0.50
        note = "Estimated Uncorrected Endurance Limit (Se' = 0.5 * Sut)"
    elif "aluminum" in name or "polymer" in cat:
        endurance_limit = req.tensile_strength * 0.35
        note = "Estimated Fatigue Strength at 5e8 cycles (Sf = 0.35 * Sut)"
    else:
        endurance_limit = req.tensile_strength * 0.40
        note = "Estimated Endurance Limit (Se' = 0.4 * Sut)"
        
    return {
        "ok": True,
        "data": {
            "endurance_limit": endurance_limit,
            "note": note
        }
    }

# 6. Risk Auditor
class RiskRequest(BaseModel):
    material_name: str
    embodied_carbon: float
    cost_per_kg_inr: float
    volume_tons: float
    cbam_price_usd: float

@router.post("/risk_auditor")
def calculate_risk(req: RiskRequest):
    total_carbon_tons = req.embodied_carbon * req.volume_tons
    annual_cbam_tax_usd = total_carbon_tons * req.cbam_price_usd
    material_cost_per_kg_usd = req.cost_per_kg_inr * 0.012
    annual_material_cost_usd = material_cost_per_kg_usd * (req.volume_tons * 1000)
    
    tax_percentage = (annual_cbam_tax_usd / annual_material_cost_usd) * 100 if annual_material_cost_usd > 0 else 0
    
    name = req.material_name.lower()
    risk_level = "LOW"
    risk_color = "#4CAF50"
    risk_text = "Stable global supply chain. Low risk of tariff shocks or critical export bans under current trade laws."
    
    if "titanium" in name or "ti-" in name:
        risk_level = "CRITICAL"
        risk_color = "#F44336"
        risk_text = "**US DOE Critical Material:** High dependency on CIS region (Russia) and China. Subject to severe aerospace supply chain constraints and geopolitical export quotas."
    elif "cobalt" in name or "nickel" in name or "inconel" in name:
        risk_level = "HIGH"
        risk_color = "#FF9800"
        risk_text = "**EU Critical Raw Material:** Heavy reliance on DRC (Cobalt) and Indonesian (Nickel) refining. Subject to high price volatility and stringent ESG sourcing regulations."
    elif "aluminum" in name or "al-" in name:
        risk_level = "MEDIUM"
        risk_color = "#FFEB3B"
        risk_text = "Energy-intensive refining process. Supply stability and production costs are highly correlated with global energy macro-economics."
    elif "steel" in name:
        risk_level = "MEDIUM"
        risk_color = "#FFEB3B"
        risk_text = "Subject to heavy Section 232 tariffs, EU safeguard measures, and anti-dumping regulations. Moderate supply volatility."
    elif "copper" in name or "cu-" in name or "brass" in name or "bronze" in name:
        risk_level = "HIGH"
        risk_color = "#FF9800"
        risk_text = "**Energy Transition Risk:** Massive forecasted global deficit due to EV and grid infrastructure demand. Sourcing highly dependent on South American political stability (Chile/Peru)."

    return {
        "ok": True,
        "data": {
            "total_carbon_tons": total_carbon_tons,
            "annual_cbam_tax_usd": annual_cbam_tax_usd,
            "annual_material_cost_usd": annual_material_cost_usd,
            "tax_percentage": tax_percentage,
            "geopolitics": {
                "risk_level": risk_level,
                "risk_color": risk_color,
                "risk_text": risk_text
            }
        }
    }
