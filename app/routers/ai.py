import os
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
import groq

from app.database import get_db
from app.models import Material, User
from app.auth import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Advisor"])

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = groq.Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

class AIRequest(BaseModel):
    prompt: str

@router.post("/advise")
def get_ai_advice(req: AIRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not client:
        raise HTTPException(status_code=500, detail="Groq API is not configured on the server.")
        
    if current_user.tier == "free":
        raise HTTPException(status_code=403, detail="AI Advisor is a Premium feature. Please upgrade to Pro or Advanced.")

    # STEP 1: Extract Constraints
    system_prompt_extract = """
You are an engineering constraint extractor. Analyze the user's request and extract any material constraints.
Respond ONLY with a raw JSON object (no markdown, no backticks).
Allowed keys (omit if not mentioned):
- "category": string (e.g. "Metal", "Polymer", "Ceramic", "Composite")
- "min_tensile": float (MPa)
- "max_cost": float (INR/kg)
- "min_thermal": float (W/mK)
- "max_temp": float (Celsius)
"""
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt_extract},
                {"role": "user", "content": req.prompt}
            ],
            model="llama-3.1-8b-instant"
        )
        text = response.choices[0].message.content.strip().strip('').removeprefix('json').strip()
        constraints = json.loads(text) if text.startswith('{') else {}
    except Exception as e:
        print(f"Extraction Error: {str(e)}")
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
User request: "{req.prompt}"

Here are the top matches from our database:
{json.dumps(mat_context, indent=2)}

Write a concise, professional engineering recommendation explaining why these specific materials fit the user's criteria. Mention specific strengths and trade-offs. Format nicely with markdown bullet points. Do not invent materials not in the list.
"""

    try:
        final_response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert materials engineering advisor."},
                {"role": "user", "content": advisory_prompt}
            ],
            model="llama-3.1-70b-versatile"
        )
        return {
            "response": final_response.choices[0].message.content,
            "materials": mat_context
        }
    except Exception as e:
        print(f"GROQ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate AI recommendation. Error: {str(e)}")
