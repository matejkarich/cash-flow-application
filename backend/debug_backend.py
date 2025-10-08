#!/usr/bin/env python3
"""
Debug backend startup issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    
    try:
        print("  - Testing database imports...")
        from app.core.database import engine, create_tables, get_db
        print("    ✅ Database imports OK")
    except Exception as e:
        print(f"    ❌ Database import error: {e}")
        return False
    
    try:
        print("  - Testing model imports...")
        from app.models import User, Category, CreditCard, RewardRule, Transaction
        print("    ✅ Model imports OK")
    except Exception as e:
        print(f"    ❌ Model import error: {e}")
        return False
    
    try:
        print("  - Testing schema imports...")
        from app.schemas import TransactionCreate, CategoryCreate
        print("    ✅ Schema imports OK")
    except Exception as e:
        print(f"    ❌ Schema import error: {e}")
        return False
    
    try:
        print("  - Testing service imports...")
        from app.services.visualization_service import VisualizationService
        print("    ✅ Service imports OK")
    except Exception as e:
        print(f"    ❌ Service import error: {e}")
        return False
    
    try:
        print("  - Testing API imports...")
        from app.api import visualizations, transactions, categories
        print("    ✅ API imports OK")
    except Exception as e:
        print(f"    ❌ API import error: {e}")
        return False
    
    try:
        print("  - Testing main app import...")
        from app.main import app
        print("    ✅ Main app import OK")
    except Exception as e:
        print(f"    ❌ Main app import error: {e}")
        return False
    
    return True

def test_database():
    """Test database operations"""
    print("🗄️ Testing database...")
    
    try:
        from app.core.database import create_tables, SessionLocal
        from app.models import User
        
        print("  - Creating tables...")
        create_tables()
        print("    ✅ Tables created")
        
        print("  - Testing database connection...")
        db = SessionLocal()
        user_count = db.query(User).count()
        print(f"    ✅ Database connection OK (users: {user_count})")
        db.close()
        
        return True
    except Exception as e:
        print(f"    ❌ Database error: {e}")
        return False

def main():
    """Run all debug tests"""
    print("🔍 Backend Debug Tool")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    # Test database
    if not test_database():
        print("\n❌ Database tests failed!")
        return False
    
    print("\n✅ All tests passed! Backend should start successfully.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
