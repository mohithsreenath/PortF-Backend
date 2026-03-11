from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.deps import get_db
from app.models import Admin
from app.schemas import AdminRegister, AdminLogin, TokenResponse, AdminResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.auth import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ─── POST /admin/register ─────────────────────────────────────────
@router.post("/register", response_model=AdminResponse, status_code=201)
async def register_admin(
    payload: AdminRegister,
    db: AsyncSession = Depends(get_db)
):
    # Check if username already exists
    existing = await db.execute(select(Admin).where(Admin.username == payload.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check if email already exists
    existing_email = await db.execute(select(Admin).where(Admin.email == payload.email))
    if existing_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    admin = Admin(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return admin


# ─── POST /admin/login ────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
async def login_admin(
    payload: AdminLogin,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Admin).where(Admin.username == payload.username))
    admin = result.scalar_one_or_none()

    if not admin or not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(data={"sub": admin.id})
    return {"access_token": token, "token_type": "bearer"}


# ─── GET /admin/me ────────────────────────────────────────────────
@router.get("/me", response_model=AdminResponse)
async def get_me(current_admin: Admin = Depends(get_current_admin)):
    return current_admin