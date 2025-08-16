from sqlalchemy import Column, String, ForeignKey, Numeric, Boolean, Text, Integer, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid
from typing import Dict, Any


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    bank = Column(String(100), nullable=False)
    card_type = Column(String(50), default="credit")  # credit, debit, charge
    last_four = Column(String(4))
    annual_fee = Column(Numeric(10, 2), default=0)
    active = Column(Boolean, default=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Card details
    credit_limit = Column(Numeric(10, 2))
    statement_day = Column(Integer)  # Day of month when statement closes
    due_day = Column(Integer)  # Day of month when payment is due
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    reward_rules = relationship("RewardRule", back_populates="credit_card", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="credit_card")
    user = relationship("User", back_populates="credit_cards")
    
    def __repr__(self):
        return f"<CreditCard(id={self.id}, name={self.name}, bank={self.bank})>"
    
    def calculate_rewards(self, category: str, amount: float) -> float:
        """Calculate rewards for a given category and amount"""
        applicable_rules = [rule for rule in self.reward_rules if rule.matches_category(category)]
        if not applicable_rules:
            # Find default rule
            default_rules = [rule for rule in self.reward_rules if rule.category.lower() in ['default', 'all', 'general']]
            if default_rules:
                return default_rules[0].calculate_points(amount)
            return amount * 1.0  # Default 1x points
        
        # Use the highest rate for the category
        best_rule = max(applicable_rules, key=lambda x: x.rate)
        return best_rule.calculate_points(amount)


class RewardRule(Base):
    __tablename__ = "reward_rules"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    credit_card_id = Column(String, ForeignKey("credit_cards.id"), nullable=False)
    category = Column(String(100), nullable=False)  # dining, travel, groceries, gas, etc.
    rate = Column(Numeric(5, 2), nullable=False)  # Points per dollar (e.g., 2.0 for 2x)
    cap = Column(Numeric(10, 2))  # Spending cap for this rate (quarterly/yearly)
    cap_period = Column(String(20), default="none")  # quarterly, yearly, monthly, none
    bonus_rate = Column(Numeric(5, 2))  # Bonus rate for special periods
    bonus_active = Column(Boolean, default=False)
    description = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    credit_card = relationship("CreditCard", back_populates="reward_rules")
    
    def __repr__(self):
        return f"<RewardRule(id={self.id}, category={self.category}, rate={self.rate})>"
    
    def matches_category(self, category: str) -> bool:
        """Check if this rule applies to the given category"""
        category_lower = category.lower()
        rule_category_lower = self.category.lower()
        
        # Direct match
        if category_lower == rule_category_lower:
            return True
        
        # Common category mappings
        category_mappings = {
            'dining': ['restaurant', 'food', 'dining', 'fast food'],
            'travel': ['airline', 'hotel', 'rental car', 'travel', 'uber', 'lyft'],
            'groceries': ['grocery', 'supermarket', 'food store'],
            'gas': ['gas', 'fuel', 'gas station', 'gasoline'],
            'general': ['all', 'default', 'everything'],
        }
        
        for rule_cat, keywords in category_mappings.items():
            if rule_category_lower == rule_cat:
                return any(keyword in category_lower for keyword in keywords)
        
        return False
    
    def calculate_points(self, amount: float) -> float:
        """Calculate points for a given amount"""
        rate_to_use = self.bonus_rate if self.bonus_active and self.bonus_rate else self.rate
        
        if self.cap and self.cap > 0:
            # For now, assume we haven't hit the cap - this would need tracking in production
            return amount * float(rate_to_use)
        
        return amount * float(rate_to_use)
    
    @property
    def effective_rate(self) -> float:
        """Get the current effective rate (including bonuses)"""
        return float(self.bonus_rate if self.bonus_active and self.bonus_rate else self.rate)