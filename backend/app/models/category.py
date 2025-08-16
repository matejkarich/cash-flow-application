from sqlalchemy import Column, String, ForeignKey, Numeric, Text, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid


class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_id = Column(String, ForeignKey("categories.id"), nullable=True)
    color = Column(String(7), default="#3498db")  # Hex color code
    icon = Column(String(50), default="category")  # Icon name/class
    sort_order = Column(Integer, default=0)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Budget settings
    budget_limit = Column(Numeric(10, 2), nullable=True)
    budget_period = Column(String(20), default="monthly")  # monthly, yearly, weekly
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    transactions = relationship("Transaction", foreign_keys="Transaction.category_id", back_populates="category")
    user = relationship("User", back_populates="categories")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, parent_id={self.parent_id})>"
    
    @property
    def is_parent(self) -> bool:
        """Check if this category has children"""
        return len(self.children) > 0
    
    @property
    def is_subcategory(self) -> bool:
        """Check if this category is a subcategory"""
        return self.parent_id is not None
    
    @property
    def full_path(self) -> str:
        """Get full category path (e.g., 'Food > Groceries')"""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def get_all_children_ids(self) -> list:
        """Get all descendant category IDs"""
        children_ids = [child.id for child in self.children]
        for child in self.children:
            children_ids.extend(child.get_all_children_ids())
        return children_ids