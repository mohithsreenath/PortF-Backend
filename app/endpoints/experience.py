from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models import Experience, Admin
from app.schemas import ExperienceCreate, ExperienceUpdate, ExperienceResponse
from app.db.deps import get_db
from app.core.auth import get_current_admin

router = APIRouter(prefix="/experience", tags=["Experience"])


# ─── GET /experience ────────────────── PUBLIC ────────────────────
@router.get("/", response_model=List[ExperienceResponse])
async def list_experience(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Experience).order_by(Experience.created_at.desc()))
    return result.scalars().all()


# ─── GET /experience/{id} ───────────── PUBLIC ────────────────────
@router.get("/{experience_id}", response_model=ExperienceResponse)
async def get_experience(experience_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Experience).where(Experience.id == experience_id))
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    return exp


# ─── POST /experience ───────────────── PROTECTED ─────────────────
@router.post("/", response_model=ExperienceResponse, status_code=201)
async def create_experience(
    payload: ExperienceCreate,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    exp = Experience(**payload.model_dump())
    db.add(exp)
    await db.commit()
    await db.refresh(exp)
    return exp


# ─── PUT /experience/{id} ───────────── PROTECTED ─────────────────
@router.put("/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: str,
    payload: ExperienceUpdate,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(Experience).where(Experience.id == experience_id))
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(exp, field, value)

    await db.commit()
    await db.refresh(exp)
    return exp


# ─── DELETE /experience/{id} ────────── PROTECTED ─────────────────
@router.delete("/{experience_id}", status_code=204)
async def delete_experience(
    experience_id: str,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(Experience).where(Experience.id == experience_id))
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    await db.delete(exp)
    await db.commit()