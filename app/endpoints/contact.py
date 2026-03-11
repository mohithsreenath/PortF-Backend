from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models import ContactMessage, Admin
from app.schemas import ContactCreate, ContactResponse
from app.db.deps import get_db
from app.core.auth import get_current_admin

router = APIRouter(prefix="/contact", tags=["Contact"])


# ─── POST /contact ──────────────────── PUBLIC ────────────────────
# Anyone from portfolio can send a message
@router.post("/", response_model=ContactResponse, status_code=201)
async def send_message(
    payload: ContactCreate,
    db: AsyncSession = Depends(get_db)
):
    message = ContactMessage(**payload.model_dump())
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


# ─── GET /contact ───────────────────── PROTECTED ─────────────────
# Only admin can read messages
@router.get("/", response_model=List[ContactResponse])
async def list_messages(
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(ContactMessage).order_by(ContactMessage.created_at.desc()))
    return result.scalars().all()


# ─── PATCH /contact/{id}/read ───────── PROTECTED ─────────────────
# Mark message as read
@router.patch("/{message_id}/read", response_model=ContactResponse)
async def mark_as_read(
    message_id: str,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(ContactMessage).where(ContactMessage.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    message.is_read = True
    await db.commit()
    await db.refresh(message)
    return message


# ─── DELETE /contact/{id} ───────────── PROTECTED ─────────────────
@router.delete("/{message_id}", status_code=204)
async def delete_message(
    message_id: str,
    db: AsyncSession = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(ContactMessage).where(ContactMessage.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    await db.delete(message)
    await db.commit()