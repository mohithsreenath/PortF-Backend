# app/endpoints/blogs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models import Blog, Admin
from app.schemas import BlogCreate, BlogUpdate, BlogResponse
from app.db.deps import get_db
from app.core.auth import get_current_admin

router = APIRouter(prefix="/blogs", tags=["Blogs"])


# ─── GET /blogs ─────────────────────── PUBLIC ────────────────────
@router.get("/", response_model=List[BlogResponse])
async def list_blogs(
    published_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    query = select(Blog)
    if published_only:
        query = query.where(Blog.published == True)
    query = query.order_by(Blog.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


# ─── GET /blogs/{slug} ──────────────── PUBLIC ────────────────────
@router.get("/{slug}", response_model=BlogResponse)
async def get_blog(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.slug == slug))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


# ─── POST /blogs ────────────────────── PROTECTED ─────────────────
@router.post("/", response_model=BlogResponse, status_code=201)
async def create_blog(
    payload: BlogCreate,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    existing = await db.execute(select(Blog).where(Blog.slug == payload.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Slug already exists")

    blog = Blog(**payload.model_dump())
    db.add(blog)
    await db.commit()
    await db.refresh(blog)
    return blog


# ─── PUT /blogs/{id} ────────────────── PROTECTED ─────────────────
@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: str,
    payload: BlogUpdate,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(blog, field, value)

    await db.commit()
    await db.refresh(blog)
    return blog


# ─── DELETE /blogs/{id} ─────────────── PROTECTED ─────────────────
@router.delete("/{blog_id}", status_code=204)
async def delete_blog(
    blog_id: str,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    await db.delete(blog)
    await db.commit()