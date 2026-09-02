from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Project, ProjectItem, User
from app.schemas import ProjectCreate, ProjectOut, ProjectItemCreate, ProjectItemOut
from app.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectOut])
def get_user_projects(
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(request, db)
    
    # Optional: Enforce Pro/Advanced tier
    if current_user.tier == "free":
        raise HTTPException(status_code=403, detail="Engineering Workspaces require a Pro or Advanced tier subscription.")
        
    projects = db.query(Project).filter(Project.user_id == current_user.id).order_by(Project.created_at.desc()).all()
    
    # Attach items manually if relationship is not back_populates yet
    for proj in projects:
        proj.items = db.query(ProjectItem).filter(ProjectItem.project_id == proj.id).all()
        
    return projects

@router.post("/", response_model=ProjectOut)
def create_project(
    payload: ProjectCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(request, db)
    
    if current_user.tier == "free":
        raise HTTPException(status_code=403, detail="Engineering Workspaces require a Pro or Advanced tier subscription.")
        
    # Check limit (e.g. max 50 projects)
    count = db.query(Project).filter(Project.user_id == current_user.id).count()
    if count >= 50:
        raise HTTPException(status_code=400, detail="Maximum project limit reached.")
        
    new_proj = Project(
        user_id=current_user.id,
        name=payload.name,
        description=payload.description
    )
    db.add(new_proj)
    db.commit()
    db.refresh(new_proj)
    new_proj.items = []
    return new_proj

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(request, db)
    proj = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    db.query(ProjectItem).filter(ProjectItem.project_id == project_id).delete()
    db.delete(proj)
    db.commit()
    return {"ok": True, "message": "Project deleted"}

@router.post("/{project_id}/items", response_model=ProjectItemOut)
def add_project_item(
    project_id: int,
    payload: ProjectItemCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(request, db)
    proj = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    new_item = ProjectItem(
        project_id=project_id,
        material_id=payload.material_id,
        part_name=payload.part_name,
        volume_cm3=payload.volume_cm3
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.delete("/{project_id}/items/{item_id}")
def delete_project_item(
    project_id: int,
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(request, db)
    proj = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    item = db.query(ProjectItem).filter(ProjectItem.id == item_id, ProjectItem.project_id == project_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    db.delete(item)
    db.commit()
    return {"ok": True, "message": "Item removed"}
