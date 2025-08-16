from pydantic import BaseModel, validator
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from enum import Enum


class TransactionSource(str, Enum):
    MANUAL = "manual"
    GOOGLE_SHEETS = "google_sheets"
    BANK_IMPORT = "bank_import"


class TransactionBase(BaseModel):
    date: datetime
    amount: Decimal
    description: str
    category_id: Optional[str] = None
    subcategory_id: Optional[str] = None
    payment_method: Optional[str] = None
    credit_card_id: Optional[str] = None
    source: TransactionSource = TransactionSource.MANUAL
    verified: bool = False

    @validator('amount')
    def validate_amount(cls, v):
        if v == 0:
            raise ValueError('Amount cannot be zero')
        return v


class TransactionCreate(TransactionBase):
    user_id: str
    original_description: Optional[str] = None
    import_hash: Optional[str] = None


class TransactionUpdate(BaseModel):
    date: Optional[datetime] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    subcategory_id: Optional[str] = None
    payment_method: Optional[str] = None
    credit_card_id: Optional[str] = None
    verified: Optional[bool] = None

    @validator('amount')
    def validate_amount(cls, v):
        if v is not None and v == 0:
            raise ValueError('Amount cannot be zero')
        return v


class TransactionResponse(TransactionBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    original_description: Optional[str] = None
    import_hash: Optional[str] = None
    
    # Related data
    category_name: Optional[str] = None
    subcategory_name: Optional[str] = None
    credit_card_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class TransactionSummary(BaseModel):
    """Summary statistics for transactions"""
    total_income: Decimal
    total_expenses: Decimal
    net_amount: Decimal
    transaction_count: int
    avg_transaction_amount: Decimal
    date_range: tuple[datetime, datetime]
    
    class Config:
        from_attributes = True


class BulkTransactionImport(BaseModel):
    """Schema for bulk importing transactions"""
    transactions: List[TransactionCreate]
    skip_duplicates: bool = True
    auto_categorize: bool = True