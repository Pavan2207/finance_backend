from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum as PyEnum

class RoleEnum(str, PyEnum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

class StatusEnum(str, PyEnum):
    active = "active"
    inactive = "inactive"

class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    role: Optional[RoleEnum] = None
    status: Optional[StatusEnum] = None

class UserOut(UserBase):
    id: int
    status: StatusEnum
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

