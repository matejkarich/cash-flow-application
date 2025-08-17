#!/usr/bin/env python3
"""
Reset the database by removing all data and recreating tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, SessionLocal, Base
from app.models import User, Category, CreditCard, RewardRule, Transaction

def reset_database():
    """Drop all tables and recreate them"""
    print("🗑️ Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🏗️ Recreating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database reset complete!")
    print("Run 'python init_sample_data.py' to add sample data")

if __name__ == "__main__":
    confirm = input("⚠️  This will delete ALL data in the database. Continue? (y/N): ")
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("❌ Database reset cancelled")