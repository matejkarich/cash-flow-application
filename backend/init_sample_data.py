#!/usr/bin/env python3
"""
Initialize the database with sample data for testing the finance application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, date
from decimal import Decimal
from app.core.database import engine, SessionLocal, create_tables
from app.models import User, Category, CreditCard, RewardRule, Transaction

def create_sample_user():
    """Create a demo user"""
    user = User(
        id="demo-user-123",
        email="demo@financeapp.com",
        name="Demo User",
        default_currency="USD",
        timezone="UTC"
    )
    return user

def create_sample_categories(user_id: str):
    """Create sample categories"""
    categories = []
    
    # Income categories
    income_cat = Category(
        id="cat-income",
        name="Income",
        color="#27ae60",
        icon="work",
        user_id=user_id
    )
    categories.append(income_cat)
    
    # Food categories
    food_cat = Category(
        id="cat-food",
        name="Food",
        color="#e74c3c",
        icon="restaurant",
        user_id=user_id
    )
    categories.append(food_cat)
    
    groceries_cat = Category(
        id="cat-groceries",
        name="Groceries",
        parent_id="cat-food",
        color="#e74c3c",
        icon="shopping_cart",
        user_id=user_id
    )
    categories.append(groceries_cat)
    
    dining_cat = Category(
        id="cat-dining",
        name="Dining Out",
        parent_id="cat-food",
        color="#e74c3c",
        icon="restaurant_menu",
        user_id=user_id
    )
    categories.append(dining_cat)
    
    # Transportation
    transport_cat = Category(
        id="cat-transport",
        name="Transportation",
        color="#3498db",
        icon="directions_car",
        user_id=user_id
    )
    categories.append(transport_cat)
    
    # Entertainment
    entertainment_cat = Category(
        id="cat-entertainment",
        name="Entertainment",
        color="#9b59b6",
        icon="movie",
        user_id=user_id
    )
    categories.append(entertainment_cat)
    
    # Utilities
    utilities_cat = Category(
        id="cat-utilities",
        name="Utilities",
        color="#f39c12",
        icon="bolt",
        user_id=user_id
    )
    categories.append(utilities_cat)
    
    # Shopping
    shopping_cat = Category(
        id="cat-shopping",
        name="Shopping",
        color="#e67e22",
        icon="shopping_bag",
        user_id=user_id
    )
    categories.append(shopping_cat)
    
    # Health
    health_cat = Category(
        id="cat-health",
        name="Health",
        color="#2ecc71",
        icon="medical_services",
        user_id=user_id
    )
    categories.append(health_cat)
    
    return categories

def create_sample_credit_cards(user_id: str):
    """Create sample credit cards with reward rules"""
    cards = []
    
    # Chase Sapphire Preferred
    chase_sapphire = CreditCard(
        id="card-chase-sapphire",
        name="Chase Sapphire Preferred",
        bank="Chase",
        last_four="1234",
        annual_fee=Decimal("95.00"),
        active=True,
        user_id=user_id
    )
    cards.append(chase_sapphire)
    
    # American Express Gold
    amex_gold = CreditCard(
        id="card-amex-gold",
        name="American Express Gold",
        bank="American Express",
        last_four="5678",
        annual_fee=Decimal("250.00"),
        active=True,
        user_id=user_id
    )
    cards.append(amex_gold)
    
    return cards

def create_sample_reward_rules():
    """Create sample reward rules for credit cards"""
    rules = []
    
    # Chase Sapphire rules
    rules.extend([
        RewardRule(
            credit_card_id="card-chase-sapphire",
            category="dining",
            rate=Decimal("2.0"),
            description="2x points on dining"
        ),
        RewardRule(
            credit_card_id="card-chase-sapphire",
            category="travel",
            rate=Decimal("2.0"),
            description="2x points on travel"
        ),
        RewardRule(
            credit_card_id="card-chase-sapphire",
            category="general",
            rate=Decimal("1.0"),
            description="1x points on everything else"
        )
    ])
    
    # Amex Gold rules
    rules.extend([
        RewardRule(
            credit_card_id="card-amex-gold",
            category="dining",
            rate=Decimal("4.0"),
            description="4x points on dining"
        ),
        RewardRule(
            credit_card_id="card-amex-gold",
            category="groceries",
            rate=Decimal("4.0"),
            description="4x points on groceries"
        ),
        RewardRule(
            credit_card_id="card-amex-gold",
            category="general",
            rate=Decimal("1.0"),
            description="1x points on everything else"
        )
    ])
    
    return rules

def create_sample_transactions(user_id: str):
    """Create sample transactions"""
    transactions = []
    
    # Sample data matching the CSV
    sample_data = [
        (datetime(2024, 1, 1), "Salary Deposit", Decimal("3500.00"), "cat-income", None, "Direct Deposit"),
        (datetime(2024, 1, 2), "Grocery Store", Decimal("-125.45"), "cat-food", "cat-groceries", "card-chase-sapphire"),
        (datetime(2024, 1, 3), "Netflix Subscription", Decimal("-15.99"), "cat-entertainment", None, "card-amex-gold"),
        (datetime(2024, 1, 4), "Gas Station", Decimal("-67.89"), "cat-transport", None, "card-chase-sapphire"),
        (datetime(2024, 1, 5), "Restaurant Dinner", Decimal("-89.32"), "cat-food", "cat-dining", "card-amex-gold"),
        (datetime(2024, 1, 6), "Electric Bill", Decimal("-145.67"), "cat-utilities", None, None),
        (datetime(2024, 1, 7), "Coffee Shop", Decimal("-12.50"), "cat-food", "cat-dining", None),
        (datetime(2024, 1, 8), "Amazon Purchase", Decimal("-89.99"), "cat-shopping", None, "card-chase-sapphire"),
        (datetime(2024, 1, 9), "Gym Membership", Decimal("-49.99"), "cat-health", None, "card-chase-sapphire"),
        (datetime(2024, 1, 10), "Freelance Payment", Decimal("750.00"), "cat-income", None, None),
        (datetime(2024, 1, 15), "Grocery Store", Decimal("-98.76"), "cat-food", "cat-groceries", "card-chase-sapphire"),
        (datetime(2024, 1, 20), "Restaurant Lunch", Decimal("-45.67"), "cat-food", "cat-dining", "card-amex-gold"),
        (datetime(2024, 2, 1), "Salary Deposit", Decimal("3500.00"), "cat-income", None, "Direct Deposit"),
        (datetime(2024, 2, 2), "Grocery Store", Decimal("-134.56"), "cat-food", "cat-groceries", "card-chase-sapphire"),
        (datetime(2024, 2, 5), "Restaurant Dinner", Decimal("-95.43"), "cat-food", "cat-dining", "card-amex-gold"),
    ]
    
    for i, (date, description, amount, category_id, subcategory_id, card_id) in enumerate(sample_data):
        transaction = Transaction(
            id=f"trans-{i+1:03d}",
            date=date,
            amount=amount,
            description=description,
            category_id=category_id,
            subcategory_id=subcategory_id,
            credit_card_id=card_id,
            source="manual",
            verified=True,
            user_id=user_id
        )
        transactions.append(transaction)
    
    return transactions

def init_database():
    """Initialize database with sample data"""
    print("Creating database tables...")
    create_tables()
    
    print("Creating sample data...")
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_user = db.query(User).filter(User.email == "demo@financeapp.com").first()
        
        if existing_user:
            print("✅ Sample data already exists! Skipping initialization.")
            print(f"   - User: {existing_user.name}")
            
            # Count existing data
            categories_count = db.query(Category).filter(Category.user_id == existing_user.id).count()
            cards_count = db.query(CreditCard).filter(CreditCard.user_id == existing_user.id).count()
            transactions_count = db.query(Transaction).filter(Transaction.user_id == existing_user.id).count()
            
            print(f"   - {categories_count} categories")
            print(f"   - {cards_count} credit cards")
            print(f"   - {transactions_count} transactions")
            return
        
        # Create user
        user = create_sample_user()
        db.add(user)
        
        # Create categories
        categories = create_sample_categories(user.id)
        for category in categories:
            db.add(category)
        
        # Create credit cards
        cards = create_sample_credit_cards(user.id)
        for card in cards:
            db.add(card)
        
        # Create reward rules
        rules = create_sample_reward_rules()
        for rule in rules:
            db.add(rule)
        
        # Create transactions
        transactions = create_sample_transactions(user.id)
        for transaction in transactions:
            db.add(transaction)
        
        # Commit all data
        db.commit()
        print(f"✅ Successfully created sample data:")
        print(f"   - 1 user")
        print(f"   - {len(categories)} categories")
        print(f"   - {len(cards)} credit cards")
        print(f"   - {len(rules)} reward rules")
        print(f"   - {len(transactions)} transactions")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()