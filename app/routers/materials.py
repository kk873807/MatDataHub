"""
Materials API routes.

Endpoints:
    GET  /materials          - List all materials (paginated, filterable)
    GET  /materials/search   - Full-text search by name/grade/applications
    GET  /materials/{id}     - Get one material by ID
    POST /materials          - Add a new material
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.database import get_db
from app.models import Material
from app.schemas import MaterialCreate, MaterialResponse, MaterialListResponse

router = APIRouter(prefix="/materials", tags=["Materials"])


# ──────────────────────────────────────────────
# GET /materials  — List + Filter
# ──────────────────────────────────────────────
@router.get("/", response_model=MaterialListResponse)
def list_materials(
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=400, description="Items per page"),
    # Filters
    category: Optional[str] = Query(None, description="Filter by category: Metal, Polymer, Ceramic, Composite"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    # Property range filters
    min_tensile: Optional[float] = Query(None, ge=0, description="Minimum tensile strength (MPa)"),
    max_cost: Optional[float] = Query(None, ge=0, description="Maximum cost per kg"),
    min_thermal_conductivity: Optional[float] = Query(None, ge=0, description="Minimum thermal conductivity W/(m*K)"),
    # Sorting
    sort_by: Optional[str] = Query("name", description="Sort by field name"),
    db: Session = Depends(get_db),
):
    """
    List materials with optional filters.

    Example:
        GET /materials?category=Metal&min_tensile=500&page=1&per_page=10
    """
    query = db.query(Material)

    # Apply filters
    if category:
        query = query.filter(Material.category.ilike(f"%{category}%"))
    if subcategory:
        query = query.filter(Material.subcategory.ilike(f"%{subcategory}%"))
    if min_tensile is not None:
        query = query.filter(Material.tensile_strength_min >= min_tensile)
    if max_cost is not None:
        query = query.filter(Material.cost_per_kg_max <= max_cost)
    if min_thermal_conductivity is not None:
        query = query.filter(Material.thermal_conductivity >= min_thermal_conductivity)

    # Sorting
    sort_column = getattr(Material, sort_by, Material.name)
    query = query.order_by(sort_column)

    # Get total count (before pagination)
    total = query.count()

    # Paginate
    offset = (page - 1) * per_page
    materials = query.offset(offset).limit(per_page).all()

    return MaterialListResponse(
        total=total,
        page=page,
        per_page=per_page,
        materials=materials,
    )


# ──────────────────────────────────────────────
# GET /materials/search  — Full-text search
# ──────────────────────────────────────────────
@router.get("/search", response_model=MaterialListResponse)
def search_materials(
    q: str = Query(..., min_length=1, description="Search query (searches name, grade, applications, equivalent_grades)"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=400),
    db: Session = Depends(get_db),
):
    """
    Search materials by keyword across multiple fields.

    Example:
        GET /materials/search?q=stainless
        GET /materials/search?q=corrosion resistant
    """
    search_term = f"%{q}%"

    query = db.query(Material).filter(
        or_(
            Material.name.ilike(search_term),
            Material.grade.ilike(search_term),
            Material.applications.ilike(search_term),
            Material.equivalent_grades.ilike(search_term),
            Material.description.ilike(search_term),
            Material.standard.ilike(search_term),
        )
    )

    total = query.count()
    offset = (page - 1) * per_page
    materials = query.order_by(Material.name).offset(offset).limit(per_page).all()

    return MaterialListResponse(
        total=total,
        page=page,
        per_page=per_page,
        materials=materials,
    )


# ──────────────────────────────────────────────
# GET /materials/{id}  — Get one
# ──────────────────────────────────────────────
@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(material_id: int, db: Session = Depends(get_db)):
    """
    Get a single material by its ID.

    Example:
        GET /materials/42
    """
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail=f"Material with id {material_id} not found")
    return material


# ──────────────────────────────────────────────
# POST /materials  — Create one
# ──────────────────────────────────────────────
@router.post("/", response_model=MaterialResponse, status_code=201)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    """
    Add a new material to the database.

    Used by the scraper to insert materials, or for manual entry.
    """
    db_material = Material(**material.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material
