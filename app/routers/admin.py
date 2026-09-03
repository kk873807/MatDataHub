"""
Admin routes — approve/reject tier upgrade requests.
Gated by a shared secret (ADMIN_SECRET env var) sent as X-Admin-Secret header.
This is a single-operator gate, not full RBAC.
"""
import os
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth import generate_api_key
from app.schemas import PendingRequestOut, AdminActionResponse

router = APIRouter(prefix="/admin", tags=["Admin"])
ADMIN_SECRET = os.getenv("ADMIN_SECRET")


def verify_admin(x_admin_secret: str = Header(...)):
    if not ADMIN_SECRET:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Admin access not configured.")
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid admin credentials.")
    return True


@router.get("/upgrade-requests", response_model=list[PendingRequestOut])
def list_pending_requests(_: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.upgrade_status == "pending").order_by(User.requested_at.asc()).all()
    return [
        PendingRequestOut(
            id=u.id, email=u.email, name=u.name, current_tier=u.tier,
            requested_tier=u.requested_tier, requested_at=u.requested_at,
        ) for u in users
    ]


@router.post("/upgrade-requests/{user_id}/approve", response_model=AdminActionResponse)
def approve_request(user_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    if user.upgrade_status != "pending":
        raise HTTPException(400, "This user has no pending request.")

    new_tier = user.requested_tier
    user.tier = new_tier
    if new_tier == "advanced" and not user.api_key:
        user.api_key = generate_api_key()
    user.requested_tier = None
    user.upgrade_status = None
    user.requested_at = None
    db.commit()
    db.refresh(user)

    return AdminActionResponse(message=f"Approved. {user.email} is now on {new_tier}.", user_email=user.email, tier=user.tier)


@router.post("/upgrade-requests/{user_id}/reject", response_model=AdminActionResponse)
def reject_request(user_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    if user.upgrade_status != "pending":
        raise HTTPException(400, "This user has no pending request.")

    rejected = user.requested_tier
    user.requested_tier = None
    user.upgrade_status = None
    user.requested_at = None
    db.commit()

    return AdminActionResponse(message=f"Rejected {user.email}'s request for {rejected}.", user_email=user.email, tier=user.tier)

@router.post("/users/{user_id}/block")
def block_user(user_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: block a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    user.is_blocked = True
    db.commit()
    return {"message": f"User {user.email} blocked."}


from pydantic import BaseModel
import groq
import json
from app.models import Material

class ScrapeRequest(BaseModel):
    query: str

@router.post("/scraper/ai")
def run_ai_scraper(req: ScrapeRequest, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """
    Advanced AI Pipeline that synthesizes standard engineering properties
    for any requested material family and seeds it directly into the database.
    """
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    if not GROQ_API_KEY:
        raise HTTPException(500, "GROQ_API_KEY not configured.")
        
    client = groq.Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
    You are an expert materials science database crawler. 
    Generate highly accurate engineering properties for the following materials/family requested by the user: '{req.query}'.
    Generate at least 3-10 specific grades if a family is requested (e.g., if aluminum, generate 6061-T6, 7075-T6, etc. If Inconel, generate 600, 625, 718, etc.).
    
    Output ONLY a raw JSON array of objects with these exact keys (use realistic numbers, use null if unknown):
    [
      {{
        "name": "String (e.g. Inconel 718)",
        "category": "Metal",
        "subcategory": "Nickel Superalloy",
        "grade": "718",
        "standard": "String",
        "density": Float (g/cm3),
        "tensile_strength_min": Float (MPa),
        "tensile_strength_max": Float (MPa),
        "yield_strength_min": Float (MPa),
        "yield_strength_max": Float (MPa),
        "elongation": Float (%),
        "hardness": "String",
        "elastic_modulus": Float (GPa),
        "thermal_conductivity": Float (W/mK),
        "specific_heat": Float (J/kgK),
        "melting_point_min": Float (Celsius),
        "max_service_temp": Float (Celsius),
        "cost_per_kg_min": Float (INR per kg, approx realistic),
        "cost_per_kg_max": Float (INR per kg, approx realistic),
        "applications": "String, comma separated",
        "description": "Short description"
      }}
    ]
    Do not include markdown backticks or any other text. Output RAW JSON ONLY.
    """
    
    try:
        models = [
            "groq/compound",
            "openai/gpt-oss-20b", 
            "qwen/qwen3.6-27b"
        ]
        raw_text = None
        last_error = None
        for model in models:
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a machine that outputs raw JSON data without any conversational text."},
                        {"role": "user", "content": prompt}
                    ],
                    model=model,
                    temperature=0.1
                )
                raw_text = response.choices[0].message.content.strip()
                break
            except Exception as e:
                last_error = e
                continue
                
        if not raw_text:
            raise last_error
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        data = json.loads(raw_text.strip())
        
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array.")
            
        added_count = 0
        added_names = []
        for mat in data:
            # Check if exists
            exists = db.query(Material).filter(Material.name == mat.get("name")).first()
            if not exists:
                new_mat = Material(
                    name=mat.get("name"),
                    category=mat.get("category", "Metal"),
                    subcategory=mat.get("subcategory"),
                    grade=mat.get("grade"),
                    standard=mat.get("standard"),
                    density=mat.get("density"),
                    tensile_strength_min=mat.get("tensile_strength_min"),
                    tensile_strength_max=mat.get("tensile_strength_max"),
                    yield_strength_min=mat.get("yield_strength_min"),
                    yield_strength_max=mat.get("yield_strength_max"),
                    elongation=mat.get("elongation"),
                    hardness=mat.get("hardness"),
                    elastic_modulus=mat.get("elastic_modulus"),
                    thermal_conductivity=mat.get("thermal_conductivity"),
                    specific_heat=mat.get("specific_heat"),
                    melting_point_min=mat.get("melting_point_min"),
                    max_service_temp=mat.get("max_service_temp"),
                    cost_per_kg_min=mat.get("cost_per_kg_min"),
                    cost_per_kg_max=mat.get("cost_per_kg_max"),
                    applications=mat.get("applications"),
                    description=mat.get("description"),
                    source_name="AI Pipeline (Llama 70B)",
                    is_verified=True
                )
                db.add(new_mat)
                added_names.append(mat.get("name"))
                added_count += 1
                
        db.commit()
        return {"ok": True, "message": f"Successfully scraped and added {added_count} materials.", "materials": added_names}
        
    except Exception as e:
        print(e)
        raise HTTPException(500, f"AI Scraper Error: {str(e)}")

@router.get("/test-smtp")
def test_smtp_connection(_: bool = Depends(verify_admin)):
    import smtplib
    import os
    sender_email = os.getenv("SMTP_EMAIL", "")
    sender_password = os.getenv("SMTP_PASSWORD", "")
    
    if not sender_password:
        return {"status": "error", "message": "SMTP_PASSWORD is empty or not loaded by the server."}
        
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.quit()
        return {"status": "success", "message": f"Successfully authenticated as {sender_email}!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
