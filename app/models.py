"""
Database models for MatDataHub.
These define the actual tables that store engineering material data.
"""
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, Boolean, Index
)
from sqlalchemy.sql import func

from app.database import Base


class Material(Base):
    """
    Core table: one row = one engineering material.
    
    Example row:
        name = "AISI 304 Stainless Steel"
        category = "Metal"
        subcategory = "Stainless Steel"
        grade = "304"
        standard = "ASTM A240"
    """
    __tablename__ = "materials"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ---- Identity ----
    name = Column(String(200), nullable=False, index=True)          # "AISI 304 Stainless Steel"
    category = Column(String(50), nullable=False, index=True)       # Metal, Polymer, Ceramic, Composite
    subcategory = Column(String(100), nullable=True)                 # Stainless Steel, Thermoplastic, etc.
    grade = Column(String(100), nullable=True)                       # 304, 6061-T6, PA6, etc.
    standard = Column(String(200), nullable=True)                    # ASTM A240, IS 2062, JIS G3101

    # ---- Mechanical Properties ----
    density = Column(Float, nullable=True)                           # g/cm³
    tensile_strength_min = Column(Float, nullable=True)              # MPa (range: min)
    tensile_strength_max = Column(Float, nullable=True)              # MPa (range: max)
    yield_strength_min = Column(Float, nullable=True)                # MPa (range: min)
    yield_strength_max = Column(Float, nullable=True)                # MPa (range: max)
    elongation = Column(Float, nullable=True)                        # % at break
    hardness = Column(String(50), nullable=True)                     # "85 HRB", "200 HV" (varies by scale)
    elastic_modulus = Column(Float, nullable=True)                   # GPa

    # ---- Thermal Properties ----
    thermal_conductivity = Column(Float, nullable=True)              # W/(m·K)
    specific_heat = Column(Float, nullable=True)                     # J/(kg·K)
    melting_point_min = Column(Float, nullable=True)                 # °C
    melting_point_max = Column(Float, nullable=True)                 # °C
    max_service_temp = Column(Float, nullable=True)                  # °C

    # ---- Cost & Sourcing ----
    cost_per_kg_min = Column(Float, nullable=True)                   # ₹/kg (range: min)
    cost_per_kg_max = Column(Float, nullable=True)                   # ₹/kg (range: max)
    cost_currency = Column(String(3), default="INR")                 # ISO currency code

    # ---- Descriptive Fields ----
    applications = Column(Text, nullable=True)                       # "Automotive, Kitchen sinks, Chemical tanks"
    equivalent_grades = Column(Text, nullable=True)                  # "SUS 304 (JIS), X5CrNi18-10 (EN)"
    composition = Column(Text, nullable=True)                        # "Fe 66-74%, Cr 18-20%, Ni 8-10.5%"
    description = Column(Text, nullable=True)                        # General notes

    # ---- Data Source ----
    source_url = Column(String(500), nullable=True)                  # Where we scraped this from
    source_name = Column(String(100), nullable=True)                 # "MatWeb", "MakeItFrom", "ASTM"
    is_verified = Column(Boolean, default=False)                     # Manually reviewed?

    # ---- Timestamps ----
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ---- Indexes for fast search ----
    __table_args__ = (
        Index("ix_materials_category_subcategory", "category", "subcategory"),
        Index("ix_materials_name_grade", "name", "grade"),
    )

    def __repr__(self):
        return f"<Material(id={self.id}, name='{self.name}', grade='{self.grade}')>"
