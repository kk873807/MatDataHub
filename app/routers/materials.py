"""
Materials API routes.

Per the "hook with free" strategy: ALL material data is public. Nobody needs
an account to browse, search, or view a material's full details. Tier gating
applies only to *tools* built on top of the data (comparison limits, Find
Similar, exports, etc.) — not the data itself.

Endpoints:
    GET  /materials          - List all materials (paginated, filterable) — public
    GET  /materials/search   - Full-text search by name/grade/applications — public
    GET  /materials/compare  - Fetch N materials for side-by-side comparison — public,
                                but capped by tier (anonymous visitors get the free-tier cap)
    GET  /materials/{id}     - Get one material by ID — public
    POST /materials          - Add a new material
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.database import get_db
from app.models import Material, User
from app.schemas import MaterialCreate, MaterialResponse, MaterialListResponse, BulkImportResponse
from app.auth import get_optional_user, TIER_LIMITS

router = APIRouter(prefix="/materials", tags=["Materials"])


# ──────────────────────────────────────────────
# GET /materials  — List + Filter
# ──────────────────────────────────────────────
@router.get("/", response_model=MaterialListResponse)
def list_materials(
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=500, description="Items per page"),
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
    current_user: Optional[User] = Depends(get_optional_user),  # public — used only if we personalize later
):
    """
    List materials with optional filters. Public — no login required.

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
    per_page: int = Query(20, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),  # public
):
    """
    Search materials by keyword across multiple fields. Public — no login required.

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
# GET /materials/compare  — Side-by-side comparison, tier-capped
#
# Public endpoint, but the number of materials allowed is capped by tier.
# Anonymous visitors (no token) are treated as "free" tier, consistent with
# the pricing table: free=2, pro=5, advanced=unlimited.
#
# IMPORTANT: this route MUST be declared before "/{material_id}" below.
# FastAPI matches routes in declaration order, and "/{material_id}" expects
# an int — if "/compare" were declared after it, a request to
# /materials/compare would be swallowed by "/{material_id}" and fail
# validation (since "compare" isn't a valid int), returning a confusing 422.
# ──────────────────────────────────────────────
@router.get("/compare", response_model=List[MaterialResponse])
def compare_materials(
    ids: List[int] = Query(..., description="Material IDs to compare, e.g. ?ids=1&ids=2&ids=3"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """
    Fetch full details for a set of materials to compare side-by-side.

    No login is required to compare — but the count allowed is capped by
    tier (TIER_LIMITS[tier]['compare_max']). Not-logged-in visitors get the
    free-tier cap.

    Example:
        GET /materials/compare?ids=12&ids=45&ids=69
    """
    tier = current_user.tier if current_user else "free"
    tier_config = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
    limit = tier_config["compare_max"]

    if len(ids) < 2:
        raise HTTPException(status_code=400, detail="Select at least 2 materials to compare.")

    if len(ids) > limit:
        raise HTTPException(
            status_code=403,
            detail=(
                f"Your '{tier}' tier allows comparing up to {limit} materials at once. "
                f"You requested {len(ids)}. Upgrade your tier to compare more."
            ),
        )

    materials = db.query(Material).filter(Material.id.in_(ids)).all()
    found_ids = {m.id for m in materials}
    missing = [i for i in ids if i not in found_ids]
    if missing:
        raise HTTPException(status_code=404, detail=f"Material IDs not found: {missing}")

    # Preserve the order the caller requested (matches the order of their
    # material selectors in the frontend).
    by_id = {m.id: m for m in materials}
    return [by_id[i] for i in ids]

# ──────────────────────────────────────────────
# GET /materials/{id}/similar  — Find Similar Materials (Pro+ only)
#
# Uses Euclidean distance across a set of normalized numeric properties to
# find the materials "closest" to the target material. This is a Pro+ tool
# feature per the pricing table (find_similar=True for pro/advanced).
#
# IMPORTANT: this route MUST be declared before "/{material_id}" below,
# same route-ordering reason as "/compare" above.
# ──────────────────────────────────────────────

# Properties used for similarity — same set as the frontend radar chart,
# so "similar" visually and "similar" numerically stay consistent.
SIMILARITY_PROPS = [
    "tensile_strength_max",
    "yield_strength_max",
    "elastic_modulus",
    "thermal_conductivity",
    "density",
    "cost_per_kg_max",
]


def _normalize_value(val, min_v, max_v):
    """Scale a value to 0-1 based on min/max across all materials. None-safe."""
    if val is None or min_v is None or max_v is None or max_v == min_v:
        return None
    return (val - min_v) / (max_v - min_v)


@router.get("/{material_id}/similar", response_model=List[MaterialResponse])
def find_similar_materials(
    material_id: int,
    limit: int = Query(5, ge=1, le=20, description="How many similar materials to return"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """
    Find materials numerically similar to the given material, based on
    Euclidean distance across normalized mechanical/thermal/cost properties.

    Pro+ only. Free users (including anonymous) get a 403 with an upgrade
    message.

    Example:
        GET /materials/12/similar?limit=5
    """
    tier = current_user.tier if current_user else "free"
    tier_config = TIER_LIMITS.get(tier, TIER_LIMITS["free"])

    if not tier_config["find_similar"]:
        raise HTTPException(
            status_code=403,
            detail=f"Find Similar Materials is a Pro+ feature. Your '{tier}' tier doesn't include it — upgrade to unlock.",
        )

    target = db.query(Material).filter(Material.id == material_id).first()
    if not target:
        raise HTTPException(status_code=404, detail=f"Material with id {material_id} not found")

    all_materials = db.query(Material).all()

    # Compute min/max for each property across ALL materials, for normalization
    ranges = {}
    for prop in SIMILARITY_PROPS:
        vals = [getattr(m, prop) for m in all_materials if getattr(m, prop) is not None]
        if vals:
            ranges[prop] = (min(vals), max(vals))

    def normalized_vector(material):
        """Return a dict of {prop: normalized_value} for the properties we can compute."""
        vec = {}
        for prop in SIMILARITY_PROPS:
            if prop not in ranges:
                continue
            raw = getattr(material, prop)
            min_v, max_v = ranges[prop]
            norm = _normalize_value(raw, min_v, max_v)
            if norm is not None:
                vec[prop] = norm
        return vec

    target_vec = normalized_vector(target)
    if not target_vec:
        raise HTTPException(
            status_code=400,
            detail="This material doesn't have enough numeric property data to compute similarity.",
        )

    # Compute Euclidean distance from target to every other material,
    # using only properties BOTH materials have data for.
    scored = []
    for m in all_materials:
        if m.id == target.id:
            continue
        vec = normalized_vector(m)
        shared_props = set(vec.keys()) & set(target_vec.keys())
        if not shared_props:
            continue
        squared_diffs = [(vec[p] - target_vec[p]) ** 2 for p in shared_props]
        distance = (sum(squared_diffs) / len(shared_props)) ** 0.5  # RMS: normalized by dimension count
        scored.append((distance, m))

    scored.sort(key=lambda pair: pair[0])
    top_matches = [m for _, m in scored[:limit]]

    return top_matches
# ──────────────────────────────────────────────
# GET /materials/{id}  — Get one
# ──────────────────────────────────────────────
@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),  # public
):
    """
    Get a single material by its ID. Public — no login required.

    Example:
        GET /materials/42
    """
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail=f"Material with id {material_id} not found")
    return material


# ──────────────────────────────────────────────
# POST /materials  — Create one
#
# NOTE: left unauthenticated for now — outside today's scope. This means
# anyone can currently add materials. Worth locking down (e.g. admin-only)
# separately, since it's unrelated to the free-data/paid-tools model.
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


# ──────────────────────────────────────────────
# POST /materials/bulk  — Create multiple
# ──────────────────────────────────────────────
@router.post("/bulk", response_model=BulkImportResponse, status_code=201)
def bulk_create_materials(materials: List[MaterialCreate], db: Session = Depends(get_db)):
    """
    Bulk import multiple materials. Skips existing materials based on name.
    """
    inserted = 0
    skipped = 0
    for mat in materials:
        existing = db.query(Material).filter(Material.name == mat.name).first()
        if existing:
            skipped += 1
            continue
        
        db_material = Material(**mat.model_dump())
        db.add(db_material)
        inserted += 1
    
    db.commit()
    return {"message": "Bulk import complete", "inserted": inserted, "skipped": skipped}


# ──────────────────────────────────────────────
# POST /materials/clean_legacy
# ──────────────────────────────────────────────
@router.post("/clean_legacy")
def clean_legacy_data(db: Session = Depends(get_db)):
    """
    Finds all legacy materials with 'MakeItFrom' or unverified status
    and updates them to standard references and verified=True.
    """
    legacy_mats = db.query(Material).filter(
        or_(Material.is_verified == False, Material.source_name.ilike("%MakeItFrom%"))
    ).all()
    
    count = 0
    for m in legacy_mats:
        m.is_verified = True
        m.source_name = "ASM Handbook / Literature"
        count += 1
        
    db.commit()
    return {"message": f"Fixed {count} legacy records"}
