from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import Category
from ..schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """Service for category operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_categories(self, user_id: str) -> List[Category]:
        """Get categories for a user"""
        return self.db.query(Category).filter(
            Category.user_id == user_id
        ).all()
    
    def get_category(self, category_id: str, user_id: str) -> Optional[Category]:
        """Get a specific category"""
        return self.db.query(Category).filter(
            Category.id == category_id,
            Category.user_id == user_id
        ).first()
    
    def create_category(self, category: CategoryCreate) -> Category:
        """Create a new category"""
        db_category = Category(**category.dict())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def update_category(self, category_id: str, user_id: str, category: CategoryUpdate) -> Optional[Category]:
        """Update a category"""
        db_category = self.get_category(category_id, user_id)
        if not db_category:
            return None
        
        update_data = category.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def delete_category(self, category_id: str, user_id: str) -> bool:
        """Delete a category"""
        db_category = self.get_category(category_id, user_id)
        if not db_category:
            return False
        
        self.db.delete(db_category)
        self.db.commit()
        return True
    
    def get_category_tree(self, user_id: str) -> List[Category]:
        """Get categories organized as a tree structure"""
        # Get all categories for the user
        categories = self.get_categories(user_id)
        
        # Return root categories (those without parents)
        return [cat for cat in categories if cat.parent_id is None]