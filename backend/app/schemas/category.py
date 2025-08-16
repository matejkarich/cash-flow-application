from pydantic import BaseModel, validator
from decimal import Decimal
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[str] = None
    color: str = "#3498db"
    icon: str = "category"
    sort_order: int = 0
    budget_limit: Optional[Decimal] = None
    budget_period: str = "monthly"

    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Category name cannot be empty')
        return v.strip()

    @validator('color')
    def validate_color(cls, v):
        if not v.startswith('#') or len(v) != 7:
            raise ValueError('Color must be a valid hex color code (e.g., #3498db)')
        return v


class CategoryCreate(CategoryBase):
    user_id: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    budget_limit: Optional[Decimal] = None
    budget_period: Optional[str] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or len(v.strip()) == 0):
            raise ValueError('Category name cannot be empty')
        return v.strip() if v else v

    @validator('color')
    def validate_color(cls, v):
        if v is not None and (not v.startswith('#') or len(v) != 7):
            raise ValueError('Color must be a valid hex color code (e.g., #3498db)')
        return v


class CategoryResponse(CategoryBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    is_parent: bool = False
    is_subcategory: bool = False
    full_path: str
    children_count: int = 0
    transaction_count: int = 0
    total_spent: Decimal = Decimal('0')
    
    class Config:
        from_attributes = True


class CategoryTree(CategoryResponse):
    """Category with nested children"""
    children: List['CategoryTree'] = []


class CategorySummary(BaseModel):
    """Category spending summary"""
    category_id: str
    category_name: str
    parent_name: Optional[str] = None
    total_amount: Decimal
    transaction_count: int
    percentage_of_total: float
    color: str


# Enable forward references for CategoryTree
CategoryTree.model_rebuild()