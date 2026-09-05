from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Project, ProjectItem, User
from app.schemas import ProjectCreate, ProjectOut, ProjectItemCreate, ProjectItemOut, ProjectBlueprintUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectOut])
def get_user_projects(
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    
    # Optional: Enforce Pro/Advanced tier
    if False:
        raise HTTPException(status_code=403, detail="Engineering Workspaces require a Pro or Advanced tier subscription.")
        
    try:
        projects = db.query(Project).filter(Project.user_id == current_user_id).order_by(Project.created_at.desc()).all()
        
        # Attach items manually if relationship is not back_populates yet
        for proj in projects:
            proj.items = db.query(ProjectItem).filter(ProjectItem.project_id == proj.id).all()
            
        return projects
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        raise HTTPException(status_code=400, detail=f"Exception: {str(e)} | Trace: {trace}")

@router.post("/", response_model=ProjectOut)
def create_project(
    payload: ProjectCreate,
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    try:
        if False:
            raise HTTPException(status_code=403, detail="Engineering Workspaces require a Pro or Advanced tier subscription.")
            
        count = db.query(Project).filter(Project.user_id == current_user_id).count()
        
        if False and count >= 3:
            raise HTTPException(status_code=403, detail="Pro tier is limited to 3 active projects. Upgrade to Advanced for unlimited workspaces.")
        elif count >= 100:
            raise HTTPException(status_code=400, detail="Maximum system project limit reached.")
            
        new_proj = Project(
            user_id=current_user_id,
            name=payload.name,
            description=payload.description
        )
        db.add(new_proj)
        db.commit()
        db.refresh(new_proj)
        new_proj.items = []
        return new_proj
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        raise HTTPException(status_code=400, detail=f"Exception: {str(e)} | Trace: {trace}")

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    proj = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user_id).first()
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
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    proj = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user_id).first()
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
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    proj = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    item = db.query(ProjectItem).filter(ProjectItem.id == item_id, ProjectItem.project_id == project_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    db.delete(item)
    db.commit()
    return {"ok": True, "message": "Item removed"}

@router.patch("/{project_id}/blueprint", response_model=ProjectOut)
def update_blueprint(
    project_id: int,
    payload: ProjectBlueprintUpdate,
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    proj = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    proj.blueprint_data = payload.blueprint_data
    db.commit()
    db.refresh(proj)
    proj.items = db.query(ProjectItem).filter(ProjectItem.project_id == proj.id).all()
    return proj
