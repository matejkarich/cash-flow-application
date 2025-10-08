#!/bin/bash

echo "🔧 Finance Analyzer Database Fix"
echo "================================"

# Navigate to project directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"

# Kill any existing processes
echo "🧹 Stopping any running servers..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Go to backend directory
cd backend

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

echo ""
echo "🔍 Step 1: Testing backend imports..."
python debug_backend.py

if [ $? -ne 0 ]; then
    echo "❌ Backend imports failed. Check the errors above."
    exit 1
fi

echo ""
echo "🗑️ Step 2: Resetting database..."
python reset_database.py

echo ""
echo "🗄️ Step 3: Initializing fresh sample data..."
python init_sample_data.py

if [ $? -ne 0 ]; then
    echo "❌ Database initialization failed."
    exit 1
fi

echo ""
echo "🚀 Step 4: Testing backend startup..."
echo "Starting backend server for 10 seconds to test..."

# Start backend in background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for startup
sleep 5

# Test if it's working
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running successfully!"
    echo "🏥 Health check response:"
    curl -s http://localhost:8000/health | python -m json.tool
else
    echo "❌ Backend failed to start properly"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Stop the test server
echo ""
echo "🛑 Stopping test server..."
kill $BACKEND_PID 2>/dev/null
sleep 2

echo ""
echo "🎉 Database fix complete!"
echo ""
echo "✅ You can now run:"
echo "   ./simple-start.sh"
echo ""
echo "Or start manually:"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000"
