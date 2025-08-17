from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..models import Transaction
from ..schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    """Service for transaction operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_transactions(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Transaction]:
        """Get transactions for a user"""
        return self.db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_transaction(self, transaction_id: str, user_id: str) -> Optional[Transaction]:
        """Get a specific transaction"""
        return self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()
    
    def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        """Create a new transaction"""
        db_transaction = Transaction(**transaction.dict())
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    
    def update_transaction(self, transaction_id: str, user_id: str, transaction: TransactionUpdate) -> Optional[Transaction]:
        """Update a transaction"""
        db_transaction = self.get_transaction(transaction_id, user_id)
        if not db_transaction:
            return None
        
        update_data = transaction.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_transaction, field, value)
        
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    
    def delete_transaction(self, transaction_id: str, user_id: str) -> bool:
        """Delete a transaction"""
        db_transaction = self.get_transaction(transaction_id, user_id)
        if not db_transaction:
            return False
        
        self.db.delete(db_transaction)
        self.db.commit()
        return True