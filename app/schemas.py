"""
Pydantic schemas for the Materials API.
These define what data looks like in API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MaterialBase(BaseModel):
    """Fields shared by create and response schemas."""
    name: str = Field(..., min_length=1, max_length=200, examples=["AISI 304 Stainless Steel"])
    category: str = Field(..., min_length=1, max_length=50, examples=["Metal"])
    subcategory: Optional[str] = Field(None, max_length=100, examples=["Stainless Steel"])
    grade: Optional[str] = Field(None, max_length=100, examples=["304"])
    standard: Optional[str] = Field(None, max_length=200, examples=["ASTM A240"])

    # Mechanical
    density: Optional[float] = Field(None, ge=0, examples=[7.93])
    tensile_strength_min: Optional[float] = Field(None, ge=0, examples=[515.0])
    tensile_strength_max: Optional[float] = Field(None, ge=0, examples=[750.0])
    yield_strength_min: Optional[float] = Field(None, ge=0, examples=[205.0])
    yield_strength_max: Optional[float] = Field(None, ge=0, examples=[310.0])
    elongation: Optional[float] = Field(None, ge=0, examples=[40.0])
    hardness: Optional[str] = Field(None, max_length=50, examples=["85 HRB"])
    elastic_modulus: Optional[float] = Field(None, ge=0, examples=[193.0])

    # Thermal
    thermal_conductivity: Optional[float] = Field(None, ge=0, examples=[16.2])
    specific_heat: Optional[float] = Field(None, ge=0, examples=[500.0])
    melting_point_min: Optional[float] = Field(None, examples=[1400.0])
    melting_point_max: Optional[float] = Field(None, examples=[1455.0])
    max_service_temp: Optional[float] = Field(None, examples=[870.0])

    # Cost
    cost_per_kg_min: Optional[float] = Field(None, ge=0, examples=[250.0])
    cost_per_kg_max: Optional[float] = Field(None, ge=0, examples=[400.0])
    cost_currency: Optional[str] = Field("INR", max_length=3)

    # Descriptive
    applications: Optional[str] = Field(None, examples=["Kitchen sinks, chemical tanks, food processing"])
    equivalent_grades: Optional[str] = Field(None, examples=["SUS 304 (JIS), X5CrNi18-10 (EN)"])
    composition: Optional[str] = Field(None, examples=["Fe 66-74%, Cr 18-20%, Ni 8-10.5%"])
    description: Optional[str] = None

    # Source
    source_url: Optional[str] = Field(None, max_length=500)
    source_name: Optional[str] = Field(None, max_length=100, examples=["MatWeb"])
    is_verified: Optional[bool] = False


class MaterialCreate(MaterialBase):
    """Schema for creating a new material (POST request body)."""
    pass


class MaterialResponse(MaterialBase):
    """Schema for returning a material (API response)."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MaterialListResponse(BaseModel):
    """Paginated list response."""
    total: int
    page: int
    per_page: int
    materials: list[MaterialResponse]


class BulkImportResponse(BaseModel):
    message: str
    inserted: int
    skipped: int


# ══════════════════════════════════════════════
#  Auth Schemas
# ══════════════════════════════════════════════

class RegisterRequest(BaseModel):
    """Schema for user registration."""
    email: str = Field(..., examples=["kishan@example.com"])
    password: str = Field(..., min_length=6, examples=["securepass123"])
    name: Optional[str] = Field(None, max_length=100, examples=["Kishan"])


class LoginRequest(BaseModel):
    """Schema for user login."""
    email: str = Field(..., examples=["kishan@example.com"])
    password: str = Field(..., examples=["securepass123"])


class TokenResponse(BaseModel):
    """Returned after successful register/login."""
    access_token: str
    token_type: str = "bearer"
    tier: str
    name: Optional[str] = None


class UserProfile(BaseModel):
    """User profile info returned by /auth/me."""
    id: int
    email: str
    name: Optional[str] = None
    tier: str
    api_key: Optional[str] = None
    created_at: Optional[datetime] = None

    # Upgrade-request state, so the frontend can show a "pending" badge
    # after a fresh /auth/me refresh (e.g. the sidebar "Check status" button).
    requested_tier: Optional[str] = None
    upgrade_status: Optional[str] = None

    model_config = {"from_attributes": True}


# ══════════════════════════════════════════════
#  Upgrade Request Schemas (user-facing)
# ══════════════════════════════════════════════

class UpgradeRequest(BaseModel):
    """Body sent by the frontend when a user requests a tier upgrade."""
    tier: str  # "pro" or "advanced"


class UpgradeRequestResponse(BaseModel):
    """
    Returned by POST /auth/upgrade.
    Note: this confirms the REQUEST was submitted — it does NOT mean the
    tier changed. The tier only changes once an admin approves it.
    """
    message: str
    upgrade_status: str
    requested_tier: str


# ══════════════════════════════════════════════
#  Admin Schemas (approval workflow)
# ══════════════════════════════════════════════

class PendingRequestOut(BaseModel):
    """One row in the admin's pending-upgrade-requests list."""
    id: int
    email: str
    name: Optional[str] = None
    current_tier: str
    requested_tier: str
    requested_at: Optional[datetime] = None


class AdminActionResponse(BaseModel):
    """Returned after an admin approves or rejects a request."""
    message: str
    user_email: str
    tier: str


# ══════════════════════════════════════════════
#  Feedback Schemas
# ══════════════════════════════════════════════

class FeedbackCreate(BaseModel):
    """Body sent by the frontend when a user submits feedback."""
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=255)
    category: str = Field("General Feedback", max_length=50)
    message: str = Field(..., min_length=3, max_length=2000, examples=["Would love a dark mode toggle!"])
    rating: Optional[int] = Field(None, ge=1, le=5)
    page_context: Optional[str] = Field(None, max_length=100, examples=["Feedback Tab"])
    parent_id: Optional[int] = Field(None, description="ID of the parent feedback if this is a reply")


class FeedbackOut(BaseModel):
    """One feedback row, as returned to the admin panel."""
    id: int
    user_id: Optional[int] = None
    helpful_votes: Optional[int] = 0
    name: Optional[str] = None
    email: Optional[str] = None
    category: str
    message: str
    rating: Optional[int] = None
    page_context: Optional[str] = None
    parent_id: Optional[int] = None
    status: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class FeedbackResponse(BaseModel):
    """Returned after successfully submitting or resolving feedback."""
    message: str
    id: int


# ── Project Schemas ──
class ProjectItemCreate(BaseModel):
    material_id: int
    part_name: str
    volume_cm3: float

class ProjectItemOut(BaseModel):
    id: int
    project_id: int
    material_id: int
    part_name: str
    volume_cm3: float
    material: MaterialResponse

    model_config = {"from_attributes": True}

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    blueprint_data: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    blueprint_data: Optional[str] = None
    created_at: Optional[datetime] = None
    items: List[ProjectItemOut] = []

    model_config = {"from_attributes": True}

class ProjectBlueprintUpdate(BaseModel):
    blueprint_data: str

class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    tier_purchased: str
    status: str
    payment_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
