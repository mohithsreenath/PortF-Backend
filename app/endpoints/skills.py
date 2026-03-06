from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models import Skill
from app.schemas import SkillCreate, SkillResponse
from app.db.deps import get_db


router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


@router.post("/", response_model=SkillResponse)
async def create_skill(
    payload: SkillCreate,
    db: AsyncSession = Depends(get_db)
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


@router.get("/", response_model=List[SkillResponse])
async def list_skills(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Skill))
    skills = result.scalars().all()

    return skills