import sys

file_path = 'app/schemas.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_schemas = """

class CustomMaterialCreate(BaseModel):
    name: str
    category: str
    density: Optional[float] = None
    tensile_strength_min: Optional[float] = None
    cost_per_kg_min: Optional[float] = None

class CustomMaterialResponse(CustomMaterialCreate):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class PriceHistoryResponse(BaseModel):
    id: int
    material_id: int
    cost_per_kg: float
    recorded_date: datetime
    class Config:
        from_attributes = True
"""

if "class CustomMaterialCreate" not in content:
    content += new_schemas
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added schemas.")
else:
    print("Schemas already exist.")
