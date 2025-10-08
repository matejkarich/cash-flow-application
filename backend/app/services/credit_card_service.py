from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import CreditCard, RewardRule
from ..schemas.credit_card import CreditCardCreate, CreditCardUpdate, RewardRuleCreate


class CreditCardService:
    """Service for credit card operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_credit_cards(self, user_id: str) -> List[CreditCard]:
        """Get credit cards for a user"""
        return self.db.query(CreditCard).filter(
            CreditCard.user_id == user_id
        ).all()
    
    def get_credit_card(self, card_id: str, user_id: str) -> Optional[CreditCard]:
        """Get a specific credit card"""
        return self.db.query(CreditCard).filter(
            CreditCard.id == card_id,
            CreditCard.user_id == user_id
        ).first()
    
    def create_credit_card(self, card: CreditCardCreate) -> CreditCard:
        """Create a new credit card"""
        # Extract reward rules from the card data
        reward_rules_data = card.reward_rules if hasattr(card, 'reward_rules') else []
        card_data = card.dict()
        card_data.pop('reward_rules', None)
        
        # Create the card
        db_card = CreditCard(**card_data)
        self.db.add(db_card)
        self.db.flush()  # Get the card ID
        
        # Create reward rules
        for rule_data in reward_rules_data:
            rule_data['credit_card_id'] = db_card.id
            db_rule = RewardRule(**rule_data)
            self.db.add(db_rule)
        
        self.db.commit()
        self.db.refresh(db_card)
        return db_card
    
    def update_credit_card(self, card_id: str, user_id: str, card: CreditCardUpdate) -> Optional[CreditCard]:
        """Update a credit card"""
        db_card = self.get_credit_card(card_id, user_id)
        if not db_card:
            return None
        
        update_data = card.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_card, field, value)
        
        self.db.commit()
        self.db.refresh(db_card)
        return db_card
    
    def delete_credit_card(self, card_id: str, user_id: str) -> bool:
        """Delete a credit card"""
        db_card = self.get_credit_card(card_id, user_id)
        if not db_card:
            return False
        
        self.db.delete(db_card)
        self.db.commit()
        return True
    
    def calculate_rewards(self, card_id: str, user_id: str, spending_data: dict) -> dict:
        """Calculate rewards for a card based on spending data"""
        card = self.get_credit_card(card_id, user_id)
        if not card:
            return {"error": "Card not found"}
        
        total_rewards = 0
        category_breakdown = {}
        
        for category, amount in spending_data.items():
            rewards = card.calculate_rewards(category, float(amount))
            total_rewards += rewards
            category_breakdown[category] = rewards
        
        return {
            "card_name": card.name,
            "total_rewards": total_rewards,
            "category_breakdown": category_breakdown
        }
