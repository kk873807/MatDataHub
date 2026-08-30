"""
Pydantic schemas for the Materials API.
These define what data looks like in API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
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
