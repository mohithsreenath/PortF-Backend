# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List


# ─── TechCategory ─────────────────────────────────────────────────
class TechCategoryCreate(BaseModel):
    name: str

class TechCategoryResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


# ─── Skill ────────────────────────────────────────────────────────
class SkillCreate(BaseModel):
    name: str
    level: int
    category_id: str

class SkillResponse(BaseModel):
    id: str
    name: str
    level: int
    category_id: str

    class Config:
        from_attributes = True


# ─── Project ──────────────────────────────────────────────────────
class SkillBrief(BaseModel):
    id: str
    name: str
    level: int

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None
    featured: bool = False
    skill_ids: List[str] = []

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None
    featured: Optional[bool] = None
    skill_ids: Optional[List[str]] = None

class ProjectResponse(BaseModel):
    id: str
    title: str
    slug: str
    description: Optional[str]
    github_url: Optional[str]
    live_url: Optional[str]
    image_url: Optional[str]
    featured: bool
    skills: List[SkillBrief] = []

    class Config:
        from_attributes = True