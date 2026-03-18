from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models import Skill, Admin
from app.schemas import SkillCreate, SkillResponse
from app.db.deps import get_db
from app.core.auth import get_current_admin 
 

router = APIRouter(prefix="/skills", tags=["Skills"])


# ─── GET /skills 
@router.get("/", response_model=List[SkillResponse])
async def list_skills(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill))
    skills = result.scalars().all()
    return skills


# ─── POST /skills 
@router.post("/", response_model=SkillResponse)
async def create_skill(
    payload: SkillCreate,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)  
):
    skill = Skill(
        name=payload.name,
        level=payload.level,
        category_id=payload.category_id
    )
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return skill


@router.delete("/{skill_id}", status_code=204)
async def delete_skill(
    skill_id: str,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    await db.delete(skill)
    await db.commit()