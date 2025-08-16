from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str
    default_currency: str = "USD"
    timezone: str = "UTC"

    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return v.strip()


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    default_currency: Optional[str] = None
    timezone: Optional[str] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or len(v.strip()) == 0):
            raise ValueError('Name cannot be empty')
        return v.strip() if v else v


class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True