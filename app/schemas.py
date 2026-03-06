from pydantic import BaseModel
from typing import Optional


class TechCategoryCreate(BaseModel):
    name: str


class TechCategoryResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


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