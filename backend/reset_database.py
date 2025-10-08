#!/usr/bin/env python3
"""
Reset the database completely - useful for debugging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sqlite3
from app.core.database import engine, create_tables
from app.models import User, Category, CreditCard, RewardRule, Transaction

def reset_database():
    """Completely reset the database"""
    print("🗑️ Resetting database...")
    
    # Get database URL
    db_url = str(engine.url)
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        if os.path.exists(db_path):
            print(f"Deleting database file: {db_path}")
            os.remove(db_path)
        else:
            print(f"Database file not found: {db_path}")
    
    # Recreate tables
    print("Creating fresh database tables...")
    create_tables()
    
    print("✅ Database reset complete!")

if __name__ == "__main__":
    reset_database()