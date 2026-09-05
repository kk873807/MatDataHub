import sys

file_path = 'app/routers/materials.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to add the imports first if missing
if "from app.models import CustomMaterial, PriceHistory" not in content:
    content = content.replace("from app.models import Material, User", "from app.models import Material, User, CustomMaterial, PriceHistory")

if "from app.schemas import CustomMaterialCreate, CustomMaterialResponse, PriceHistoryResponse" not in content:
    content = content.replace("from app.schemas import MaterialCreate,", "from app.schemas import MaterialCreate, CustomMaterialCreate, CustomMaterialResponse, PriceHistoryResponse,")

new_routes = """
# --- Custom Private Materials (Enterprise) ---
@router.post("/custom", response_model=CustomMaterialResponse)
def create_custom_material(
    mat: CustomMaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.tier != "advanced":
        raise HTTPException(status_code=403, detail="Custom Materials are exclusively available on the Advanced tier.")
    
    db_mat = CustomMaterial(**mat.model_dump(), user_id=current_user.id)
    db.add(db_mat)
    db.commit()
    db.refresh(db_mat)
    return db_mat

@router.get("/custom/mine", response_model=List[CustomMaterialResponse])
def get_my_custom_materials(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.tier != "advanced":
        return []
    return db.query(CustomMaterial).filter(CustomMaterial.user_id == current_user.id).all()

# --- Historical Price Tracking ---
@router.get("/{material_id}/price-history", response_model=List[PriceHistoryResponse])
def get_price_history(
    material_id: int,
    db: Session = Depends(get_db)
):
    # Public endpoint to fetch price graph data
    history = db.query(PriceHistory).filter(PriceHistory.material_id == material_id).order_by(PriceHistory.recorded_date.asc()).all()
    # If no history exists, mock some data based on the current cost for demo purposes
    if not history:
        mat = db.query(Material).filter(Material.id == material_id).first()
        if mat and mat.cost_per_kg_min:
            import random
            from datetime import timedelta, datetime
            now = datetime.utcnow()
            base_price = mat.cost_per_kg_min
            # Generate 12 months of fake historical volatility for demo
            history = []
            for i in range(12, 0, -1):
                past_date = now - timedelta(days=30*i)
                fluctuation = base_price * random.uniform(0.85, 1.15)
                history.append(
                    PriceHistoryResponse(
                        id=i, material_id=material_id, cost_per_kg=round(fluctuation, 2), recorded_date=past_date
                    )
                )
            # Add current price
            history.append(PriceHistoryResponse(id=0, material_id=material_id, cost_per_kg=base_price, recorded_date=now))
    return history
"""

if "@router.post(\"/custom\"" not in content:
    content += new_routes
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added custom materials and price history endpoints.")
else:
    print("Endpoints already exist.")
