from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from app.db.base import Base
import uuid


class TechCategory(Base):

    __tablename__ = "tech_categories"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(String(100), unique=True)


class Skill(Base):

    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(String(100))

    level: Mapped[int] = mapped_column(Integer)

    category_id: Mapped[str] = mapped_column(
        ForeignKey("tech_categories.id")
    )