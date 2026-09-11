from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Blog
from pydantic import BaseModel
from typing import List, Optional
from app.routers.admin import verify_admin

router = APIRouter(prefix="/blogs", tags=["Blogs"])

class BlogCreate(BaseModel):
    title: str
    date: str
    author: str
    readTime: str
    tag: str
    featured: bool
    excerpt: str
    content: str

@router.get("/")
def get_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).order_by(Blog.id.desc()).all()

@router.post("/")
def create_blog(blog: BlogCreate, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    new_blog = Blog(**blog.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete("/{blog_id}")
def delete_blog(blog_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog: raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return {"detail": "Blog deleted"}
