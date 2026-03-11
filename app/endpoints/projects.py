from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models import Project, ProjectSkill, Admin
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.db.deps import get_db
from app.core.auth import get_current_admin  

router = APIRouter(prefix="/projects", tags=["Projects"])


def _format(project: Project) -> dict:
    return {
        **{c.name: getattr(project, c.name) for c in project.__table__.columns},
        "skills": [ps.skill for ps in project.project_skills],
    }


# ─── GET /projects 
@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    featured: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Project).options(
        selectinload(Project.project_skills).selectinload(ProjectSkill.skill)
    )
    if featured is not None:
        query = query.where(Project.featured == featured)
    query = query.order_by(Project.created_at.desc())
    result = await db.execute(query)
    projects = result.scalars().all()
    return [_format(p) for p in projects]


# ─── GET /projects/{slug} 
@router.get("/{slug}", response_model=ProjectResponse)
async def get_project(slug: str, db: AsyncSession = Depends(get_db)):
    query = select(Project).options(
        selectinload(Project.project_skills).selectinload(ProjectSkill.skill)
    ).where(Project.slug == slug)
    result = await db.execute(query)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return _format(project)


# ─── POST /projects 
@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)  
):
    existing = await db.execute(select(Project).where(Project.slug == payload.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Slug already exists")

    project = Project(**payload.model_dump(exclude={"skill_ids"}))
    db.add(project)
    await db.flush()

    for skill_id in payload.skill_ids:
        db.add(ProjectSkill(project_id=project.id, skill_id=skill_id))

    await db.commit()

    query = select(Project).options(
        selectinload(Project.project_skills).selectinload(ProjectSkill.skill)
    ).where(Project.id == project.id)
    result = await db.execute(query)
    project = result.scalar_one()
    return _format(project)


# ─── PUT /projects/{id} 
@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin) 
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in payload.model_dump(exclude_unset=True, exclude={"skill_ids"}).items():
        setattr(project, field, value)

    if payload.skill_ids is not None:
        await db.execute(delete(ProjectSkill).where(ProjectSkill.project_id == project_id))
        for skill_id in payload.skill_ids:
            db.add(ProjectSkill(project_id=project_id, skill_id=skill_id))

    await db.commit()

    query = select(Project).options(
        selectinload(Project.project_skills).selectinload(ProjectSkill.skill)
    ).where(Project.id == project_id)
    result = await db.execute(query)
    project = result.scalar_one()
    return _format(project)


# ─── DELETE /projects/{id} 
@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)  
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    await db.commit()