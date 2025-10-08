#!/bin/bash

# Fix and Test Script for Finance Analyzer

echo "🔧 Fixing and testing Finance Analyzer..."

# Go to project root
cd "$(dirname "$0")"

# Kill any existing processes
echo "🧹 Cleaning up any existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Remove old virtual environment if it exists
if [ -d "backend/venv" ]; then
    echo "🗑️ Removing old virtual environment..."
    rm -rf backend/venv
fi

# Remove node_modules if it exists
if [ -d "frontend/node_modules" ]; then
    echo "🗑️ Removing old node_modules..."
    rm -rf frontend/node_modules
fi

# Clean up log files
rm -f backend.log frontend.log

echo "✅ Cleanup complete"

# Test backend setup
echo "🧪 Testing backend setup..."
cd backend

# Create fresh virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Test imports
python -c "
import sys
sys.path.append('.')
try:
    from app.core.database import create_tables
    from app.models import User, Category, Transaction
    print('✅ Backend imports working')
except Exception as e:
    print(f'❌ Backend import error: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Backend test failed"
    exit 1
fi

# Initialize database
echo "🗄️ Initializing database..."
python init_sample_data.py

if [ $? -ne 0 ]; then
    echo "❌ Database initialization failed"
    exit 1
fi

# Test frontend setup
echo "🧪 Testing frontend setup..."
cd ../frontend

# Install dependencies
npm install

if [ $? -ne 0 ]; then
    echo "❌ Frontend dependency installation failed"
    exit 1
fi

# Test build
echo "🏗️ Testing frontend build..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed"
    exit 1
fi

echo "✅ All tests passed!"
echo ""
echo "🚀 Ready to start the application!"
echo "Run ./start.sh to start both servers"