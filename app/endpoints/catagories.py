from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models import TechCategory, Admin
from app.schemas import TechCategoryCreate, TechCategoryResponse
from app.db.deps import get_db
from app.core.auth import get_current_admin  

router = APIRouter(prefix="/categories", tags=["Categories"])


# ─── GET /categories 
@router.get("/", response_model=List[TechCategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TechCategory))
    categories = result.scalars().all()
    return categories


# ─── POST /categories 
@router.post("/", response_model=TechCategoryResponse)
async def create_category(
    payload: TechCategoryCreate,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)  
):
    category = TechCategory(name=payload.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category