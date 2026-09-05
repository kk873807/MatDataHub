import sys

file_path = 'app/models.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_models = """

class CustomMaterial(Base):
    __tablename__ = "custom_materials"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name = Column(String(255), index=True)
    category = Column(String(100), index=True)
    subcategory = Column(String(100), nullable=True)
    
    density = Column(Float, nullable=True)
    tensile_strength_min = Column(Float, nullable=True)
    tensile_strength_max = Column(Float, nullable=True)
    yield_strength_min = Column(Float, nullable=True)
    yield_strength_max = Column(Float, nullable=True)
    elongation_min = Column(Float, nullable=True)
    elongation_max = Column(Float, nullable=True)
    hardness_min = Column(Float, nullable=True)
    hardness_max = Column(Float, nullable=True)
    hardness_scale = Column(String(50), nullable=True)
    
    thermal_conductivity = Column(Float, nullable=True)
    specific_heat = Column(Float, nullable=True)
    melting_point = Column(Float, nullable=True)
    max_service_temp = Column(Float, nullable=True)
    
    electrical_resistivity = Column(Float, nullable=True)
    
    cost_per_kg_min = Column(Float, nullable=True)
    cost_per_kg_max = Column(Float, nullable=True)
    
    applications = Column(Text, nullable=True)
    equivalent_grades = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id", ondelete="CASCADE"), index=True)
    cost_per_kg = Column(Float, nullable=False)
    recorded_date = Column(DateTime(timezone=True), server_default=func.now())
    
    material = relationship("Material")
"""

if "class CustomMaterial" not in content:
    content += new_models
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added CustomMaterial and PriceHistory models.")
else:
    print("Models already exist.")
