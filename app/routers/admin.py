"""
Admin routes — manage users, upgrades, contributions, transactions, and AI tools.
Gated by JWT-based RBAC: only users with is_admin=True can access these endpoints.
"""
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import User, Transaction
from app.auth import generate_api_credentials, get_current_user
from app.schemas import PendingRequestOut, AdminActionResponse, AdminTransactionOut

router = APIRouter(prefix="/admin", tags=["Admin"])



def verify_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Access denied. Admin privileges required.")
    return current_user


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
        raw_key, raw_secret = generate_api_credentials()
        user.api_key = raw_key
        user.api_secret = raw_secret
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
def block_user(user_id: int, _: User = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: block a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    user.is_blocked = True
    db.commit()
    return {"message": f"User {user.email} blocked."}

@router.post("/users/{user_id}/unblock")
def unblock_user(user_id: int, _: User = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: unblock a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    if not user.is_blocked:
        raise HTTPException(400, f"{user.email} is not blocked.")
    user.is_blocked = False
    db.commit()
    return {"message": f"User {user.email} unblocked."}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: completely delete a user account and their data."""
    if user_id == admin.id:
        raise HTTPException(400, "You cannot delete your own admin account. Transfer admin rights first.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    if user.is_admin:
        raise HTTPException(400, "Cannot delete another admin. Revoke their admin rights first.")
    
    # Clean up orphan data before deleting the user
    from app.models import Feedback, Project
    db.query(Transaction).filter(Transaction.user_id == user.id).delete()
    db.query(Feedback).filter(Feedback.user_id == user.id).update({"user_id": None})
    db.query(Project).filter(Project.user_id == user.id).delete()
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user.email} has been permanently deleted."}


class AdminTransferRequest(BaseModel):
    target_email: str

@router.post("/transfer")
def transfer_admin(req: AdminTransferRequest, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    """Transfer admin rights to another user by email. The current admin keeps their rights too."""
    target = db.query(User).filter(User.email == req.target_email).first()
    if not target:
        raise HTTPException(404, f"No user found with email '{req.target_email}'.")
    if target.is_admin:
        raise HTTPException(400, f"{req.target_email} is already an admin.")
    if target.is_blocked:
        raise HTTPException(400, "Cannot grant admin rights to a blocked user.")
    
    target.is_admin = True
    db.commit()
    return {"message": f"Admin rights granted to {req.target_email}. Both accounts now have admin access."}


@router.post("/revoke/{user_id}")
def revoke_admin(user_id: int, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    """Revoke admin rights from another user. Cannot revoke your own rights."""
    if user_id == admin.id:
        raise HTTPException(400, "You cannot revoke your own admin rights.")
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(404, "User not found.")
    if not target.is_admin:
        raise HTTPException(400, f"{target.email} is not an admin.")
    
    target.is_admin = False
    db.commit()
    return {"message": f"Admin rights revoked from {target.email}."}


class AdminRevokeByEmailRequest(BaseModel):
    target_email: str

@router.post("/revoke-by-email")
def revoke_admin_by_email(req: AdminRevokeByEmailRequest, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    """Revoke admin rights from a user by email."""
    target = db.query(User).filter(User.email == req.target_email).first()
    if not target:
        raise HTTPException(404, f"No user found with email '{req.target_email}'.")
    if target.id == admin.id:
        raise HTTPException(400, "You cannot revoke your own admin rights.")
    if not target.is_admin:
        raise HTTPException(400, f"{req.target_email} is not an admin.")
    
    target.is_admin = False
    db.commit()
    return {"message": f"Admin rights revoked from {req.target_email}. They no longer have admin access."}


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
                    source_name="AI Synthesized",
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

from app.models import CustomMaterial

@router.get("/user-contributions")
def get_all_user_contributions(_: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """
    Returns all user contributions grouped by user.
    """
    materials = db.query(CustomMaterial).order_by(CustomMaterial.created_at.desc()).all()
    user_ids = {m.user_id for m in materials if m.user_id}
    users = db.query(User).filter(User.id.in_(user_ids)).all() if user_ids else []
    
    user_map = {u.id: {"id": u.id, "name": u.name or "User", "email": u.email, "tier": u.tier} for u in users}
    
    contribs = {}
    for m in materials:
        if m.user_id not in contribs:
            contribs[m.user_id] = {
                "user": user_map.get(m.user_id, {"id": m.user_id, "name": "Unknown", "email": "unknown", "tier": "free"}),
                "materials": []
            }
        contribs[m.user_id]["materials"].append({
            "id": m.id,
            "name": m.name,
            "category": m.category,
            "source_url": m.source_url,
            "status": getattr(m, "status", "pending"),
            "created_at": m.created_at
        })
        
    return list(contribs.values())

@router.post("/contributions/{contrib_id}/approve")
def approve_contribution(contrib_id: int, db: Session = Depends(get_db), _: bool = Depends(verify_admin)):
    from app.models import CustomMaterial, Material
    contrib = db.query(CustomMaterial).filter(CustomMaterial.id == contrib_id).first()
    if not contrib:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    if contrib.status == "approved":
        raise HTTPException(status_code=400, detail="Already approved")

    if contrib.source_url:
        existing = db.query(Material).filter(Material.source_url == contrib.source_url).first()
        if existing:
            raise HTTPException(status_code=400, detail="This source URL already exists in the public database! Please Reject this contribution instead.")

    # Move to public materials
    hardness_str = None
    if contrib.hardness_min and contrib.hardness_scale:
        hardness_str = f"{contrib.hardness_min} {contrib.hardness_scale}"
    elif contrib.hardness_min:
        hardness_str = str(contrib.hardness_min)

    new_mat = Material(
        name=contrib.name,
        category=contrib.category,
        subcategory=contrib.subcategory,
        grade=contrib.grade,
        standard=getattr(contrib, 'standard', None),
        source_name="User Contributed",
        description=contrib.description,
        source_url=contrib.source_url,
        elastic_modulus=contrib.elastic_modulus,
        density=contrib.density,
        yield_strength_min=contrib.yield_strength_min,
        yield_strength_max=contrib.yield_strength_max,
        tensile_strength_min=contrib.tensile_strength_min,
        tensile_strength_max=contrib.tensile_strength_max,
        elongation=contrib.elongation_min,
        hardness=hardness_str,
        thermal_conductivity=contrib.thermal_conductivity,
        specific_heat=contrib.specific_heat,
        melting_point_min=contrib.melting_point,
        max_service_temp=contrib.max_service_temp,
        cost_per_kg_min=getattr(contrib, 'cost_per_kg_min', None),
        cost_per_kg_max=getattr(contrib, 'cost_per_kg_max', None),
        applications=getattr(contrib, 'applications', None),
        is_verified=True,
    )
    db.add(new_mat)
    contrib.status = "approved"
    db.commit()
    return {"message": "Contribution approved and added to public database"}

@router.post("/contributions/{contrib_id}/reject")
def reject_contribution(contrib_id: int, db: Session = Depends(get_db), _: bool = Depends(verify_admin)):
    from app.models import CustomMaterial
    contrib = db.query(CustomMaterial).filter(CustomMaterial.id == contrib_id).first()
    if not contrib:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    if contrib.status == "approved":
        raise HTTPException(status_code=400, detail="Cannot reject a contribution that has already been approved and merged into the public database.")
    
    contrib.status = "rejected"
    db.commit()
    return {"message": "Contribution rejected"}

@router.get("/transactions", response_model=list[AdminTransactionOut])
def get_all_transactions(db: Session = Depends(get_db), _: bool = Depends(verify_admin)):
    """Fetch all platform transactions with user emails for the admin dashboard."""
    txns = db.query(Transaction, User.email).join(User, Transaction.user_id == User.id).order_by(Transaction.created_at.desc()).all()
    
    result = []
    for txn, email in txns:
        txn_dict = {
            "id": txn.id,
            "user_id": txn.user_id,
            "amount": txn.amount,
            "currency": txn.currency,
            "tier_purchased": txn.tier_purchased,
            "status": txn.status,
            "payment_id": txn.payment_id,
            "created_at": txn.created_at,
            "user_email": email
        }
        result.append(txn_dict)
    return result
