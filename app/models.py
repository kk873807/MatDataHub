"""
Database models for MatDataHub.
These define the actual tables that store engineering material data.
"""
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, Boolean, Index
)
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


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
    description = Column(Text, nullable=True)
    blueprint_data = Column(Text, nullable=True)                        # General notes

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


class User(Base):
    """
    User accounts for authentication and tier-based access.

    Tiers:
        free     - All data visible, compare 2, no export
        pro      - Compare 5, export, find similar, AI advisor
        advanced - Unlimited compare, API access, PDF reports

    Upgrade requests:
        Upgrading tiers is a manual-approval flow, not instant. When a user
        requests an upgrade, `requested_tier` and `upgrade_status` ("pending")
        are set but `tier` is NOT changed. An admin approves/rejects via the
        /admin endpoints, which is what actually updates `tier`.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)

    # Tier: "free", "pro", "advanced"
    tier = Column(String(20), default="free", nullable=False)

    # API key for programmatic access (Advanced tier only)
    api_key = Column(String(64), unique=True, nullable=True, index=True)

    # ---- Upgrade request tracking ----
    requested_tier = Column(String(20), nullable=True)               # "pro" or "advanced" while pending
    upgrade_status = Column(String(20), nullable=True)               # "pending" or None
    requested_at = Column(DateTime(timezone=True), nullable=True)    # when the request was submitted

    is_active = Column(Boolean, default=True)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', tier='{self.tier}')>"


class Feedback(Base):
    """
    User feedback / comments / bug reports / feature requests.
    user_id is nullable — anonymous (not logged in) users can also submit feedback.
    """
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, nullable=True, index=True)   # not a FK constraint, just a soft link to users.id
    name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)

    category = Column(String(50), default="General")        # Bug Report / Feature Request / General Feedback / Data Correction / Other
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)                  # 1-5, optional
    page_context = Column(String(100), nullable=True)        # which tab/page it came from

    status = Column(String(20), default="new")
    helpful_votes = Column(Integer, default=0)               # "new" or "reviewed"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Feedback(id={self.id}, category='{self.category}', status='{self.status}')>"


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    blueprint_data = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProjectItem(Base):
    __tablename__ = "project_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, index=True, nullable=False)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    part_name = Column(String(100), nullable=False)
    volume_cm3 = Column(Float, nullable=False, default=1.0)
    
    # Relationship to easily fetch material details when querying an item
    material = relationship("Material")
