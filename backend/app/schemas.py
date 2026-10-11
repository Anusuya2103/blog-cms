from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import RoleEnum


# ---------- Auth / User ----------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class LoginRequest(BaseModel):
    username: str
    password: str


# ---------- Category ----------

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Comment ----------

class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserOut

    model_config = ConfigDict(from_attributes=True)


# ---------- Post ----------

class PostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    published: bool = True
    category_ids: List[int] = []


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    published: Optional[bool] = None
    category_ids: Optional[List[int]] = None


class PostOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    summary: Optional[str]
    published: bool
    created_at: datetime
    updated_at: datetime
    author: UserOut
    categories: List[CategoryOut] = []

    model_config = ConfigDict(from_attributes=True)


class PostListOut(BaseModel):
    id: int
    title: str
    slug: str
    summary: Optional[str]
    published: bool
    created_at: datetime
    author: UserOut
    categories: List[CategoryOut] = []

    model_config = ConfigDict(from_attributes=True)


class HealthOut(BaseModel):
    status: str
    database: str
