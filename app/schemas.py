# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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


# ─── Admin ────────────────────────────────────────────────────────
class AdminRegister(BaseModel):
    username: str
    email: str
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AdminResponse(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        from_attributes = True


# ─── Experience ───────────────────────────────────────────────────
class ExperienceCreate(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    description: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    is_current: bool = False

class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: Optional[bool] = None

class ExperienceResponse(BaseModel):
    id: str
    company: str
    role: str
    location: Optional[str]
    description: Optional[str]
    start_date: str
    end_date: Optional[str]
    is_current: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Blog ─────────────────────────────────────────────────────────
class BlogCreate(BaseModel):
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    published: bool = False

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    published: Optional[bool] = None

class BlogResponse(BaseModel):
    id: str
    title: str
    slug: str
    content: str
    summary: Optional[str]
    published: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ─── Contact ──────────────────────────────────────────────────────
class ContactCreate(BaseModel):
    name: str
    email: str
    message: str

class ContactResponse(BaseModel):
    id: str
    name: str
    email: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True