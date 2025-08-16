from pydantic import BaseModel, validator
from decimal import Decimal
from typing import Optional, List
from datetime import datetime


class RewardRuleBase(BaseModel):
    category: str
    rate: Decimal
    cap: Optional[Decimal] = None
    cap_period: str = "none"
    bonus_rate: Optional[Decimal] = None
    bonus_active: bool = False
    description: Optional[str] = None

    @validator('rate')
    def validate_rate(cls, v):
        if v <= 0:
            raise ValueError('Reward rate must be positive')
        return v

    @validator('bonus_rate')
    def validate_bonus_rate(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Bonus rate must be positive')
        return v


class RewardRuleCreate(RewardRuleBase):
    credit_card_id: str


class RewardRuleUpdate(BaseModel):
    category: Optional[str] = None
    rate: Optional[Decimal] = None
    cap: Optional[Decimal] = None
    cap_period: Optional[str] = None
    bonus_rate: Optional[Decimal] = None
    bonus_active: Optional[bool] = None
    description: Optional[str] = None


class RewardRuleResponse(RewardRuleBase):
    id: str
    credit_card_id: str
    created_at: datetime
    updated_at: datetime
    effective_rate: float

    class Config:
        from_attributes = True


class CreditCardBase(BaseModel):
    name: str
    bank: str
    card_type: str = "credit"
    last_four: Optional[str] = None
    annual_fee: Decimal = Decimal('0')
    active: bool = True
    credit_limit: Optional[Decimal] = None
    statement_day: Optional[int] = None
    due_day: Optional[int] = None

    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Card name cannot be empty')
        return v.strip()

    @validator('last_four')
    def validate_last_four(cls, v):
        if v is not None and (not v.isdigit() or len(v) != 4):
            raise ValueError('Last four digits must be exactly 4 digits')
        return v

    @validator('statement_day', 'due_day')
    def validate_day(cls, v):
        if v is not None and (v < 1 or v > 31):
            raise ValueError('Day must be between 1 and 31')
        return v


class CreditCardCreate(CreditCardBase):
    user_id: str
    reward_rules: List[RewardRuleBase] = []


class CreditCardUpdate(BaseModel):
    name: Optional[str] = None
    bank: Optional[str] = None
    card_type: Optional[str] = None
    last_four: Optional[str] = None
    annual_fee: Optional[Decimal] = None
    active: Optional[bool] = None
    credit_limit: Optional[Decimal] = None
    statement_day: Optional[int] = None
    due_day: Optional[int] = None


class CreditCardResponse(CreditCardBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    reward_rules: List[RewardRuleResponse] = []
    
    # Computed fields
    total_transactions: int = 0
    total_spent: Decimal = Decimal('0')
    total_rewards_earned: float = 0.0
    
    class Config:
        from_attributes = True


class CardComparison(BaseModel):
    """Compare rewards between different cards for given spending"""
    card_id: str
    card_name: str
    total_rewards: float
    annual_fee: Decimal
    net_value: float  # rewards - annual_fee
    category_breakdown: dict[str, float]


class RewardsCalculation(BaseModel):
    """Rewards calculation for a specific spending pattern"""
    spending_by_category: dict[str, Decimal]
    comparisons: List[CardComparison]
    recommended_card_id: str
    potential_savings: float