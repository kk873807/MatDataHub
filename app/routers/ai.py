import os
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
import google.generativeai as genai
from pydantic import BaseModel

from app.database import get_db
from app.models import Material, User
from app.auth import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Advisor"])

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class AIRequest(BaseModel):
    prompt: str

@router.post("/advise")
def get_ai_advice(req: AIRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API is not configured.")
        
    if current_user.tier == "free":
        raise HTTPException(status_code=403, detail="AI Advisor is a Premium feature. Please upgrade to Pro or Advanced.")

    model = genai.GenerativeModel('gemini-1.5-flash')

    # STEP 1: Extract Constraints
    extraction_prompt = f"""
You are an engineering constraint extractor. Analyze the user's request and extract any material constraints.
Respond ONLY with a raw JSON object (no markdown, no backticks).
Allowed keys (omit if not mentioned):
- "category": string (e.g. "Metal", "Polymer", "Ceramic", "Composite")
- "min_tensile": float (MPa)
- "max_cost": float (INR/kg)
- "min_thermal": float (W/mK)
- "max_temp": float (Celsius)

User request: "{req.prompt}"
"""
    
    try:
        response = model.generate_content(extraction_prompt)
        text = response.text.strip().strip('').removeprefix('json').strip()
        constraints = json.loads(text) if text.startswith('{') else {}
    except Exception as e:
        constraints = {}

    # STEP 2: Database Query
    query = db.query(Material)
    
    if "category" in constraints and constraints["category"]:
        query = query.filter(Material.category.ilike(f"%{constraints['category']}%"))
    if "min_tensile" in constraints:
        query = query.filter(Material.tensile_strength_min >= constraints["min_tensile"])
    if "max_cost" in constraints:
        query = query.filter(Material.cost_per_kg_min <= constraints["max_cost"])
    if "min_thermal" in constraints:
        query = query.filter(Material.thermal_conductivity >= constraints["min_thermal"])
    if "max_temp" in constraints:
        query = query.filter(Material.max_service_temp >= constraints["max_temp"])
        
    results = query.limit(5).all()
    
    if not results:
        return {"response": "I couldn't find any materials in the database that match those exact constraints. Could you try relaxing some of your requirements?", "materials": []}
        
    # Serialize top results for the AI context
    mat_context = []
    for m in results:
        mat_context.append({
            "name": m.name,
            "category": m.category,
            "tensile_strength": f"{m.tensile_strength_min}-{m.tensile_strength_max} MPa",
            "cost": f"Rs. {m.cost_per_kg_min}/kg",
            "applications": m.applications
        })

    # STEP 3: Generate Recommendation
    advisory_prompt = f"""
You are a materials engineering advisor. 
User request: "{req.prompt}"

Here are the top matches from our database:
{json.dumps(mat_context, indent=2)}

Write a concise, professional engineering recommendation explaining why these specific materials fit the user's criteria. Mention specific strengths and trade-offs. Format nicely with markdown bullet points. Do not invent materials not in the list.
"""

    try:
        final_response = model.generate_content(advisory_prompt)
        return {
            "response": final_response.text,
            "materials": mat_context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate AI recommendation.")
