from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid
from decimal import Decimal


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(DateTime, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    subcategory_id = Column(String, ForeignKey("categories.id"), nullable=True)
    payment_method = Column(String, nullable=True)  # e.g., "Chase Sapphire", "Cash", "Debit"
    credit_card_id = Column(String, ForeignKey("credit_cards.id"), nullable=True)
    source = Column(String, nullable=False, default="manual")  # google_sheets, bank_import, manual
    verified = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Import metadata
    original_description = Column(Text)  # Store original bank description
    import_hash = Column(String)  # For duplicate detection
    
    # Relationships
    category = relationship("Category", foreign_keys=[category_id], back_populates="transactions")
    subcategory = relationship("Category", foreign_keys=[subcategory_id])
    credit_card = relationship("CreditCard", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, date={self.date}, amount={self.amount}, description={self.description})>"
    
    @property
    def is_income(self) -> bool:
        """Check if transaction is income (positive amount)"""
        return self.amount > 0
    
    @property
    def is_expense(self) -> bool:
        """Check if transaction is expense (negative amount)"""
        return self.amount < 0
    
    @property
    def amount_abs(self) -> Decimal:
        """Get absolute value of amount"""
        return abs(self.amount)