#!/bin/bash

echo "🔧 Quick Fix for Finance Analyzer Database Issue"

# Navigate to project directory
cd "$(dirname "$0")"

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Go to backend
cd backend

# Check if we have a virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip

# Try simple requirements first
if [ -f "requirements-simple.txt" ]; then
    pip install -r requirements-simple.txt
else
    pip install -r requirements.txt
fi

# Remove the existing database file to start fresh
if [ -f "finance.db" ]; then
    echo "🗑️ Removing existing database..."
    rm finance.db
fi

# Create .env file
echo "📝 Creating .env file..."
cat > .env << 'EOF'
DATABASE_URL=sqlite:///./finance.db
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000
EOF

# Initialize database with fresh data
echo "🗄️ Creating fresh database..."
python init_sample_data.py

if [ $? -eq 0 ]; then
    echo "✅ Database created successfully"
else
    echo "❌ Database creation failed"
    exit 1
fi

# Start backend
echo "🚀 Starting backend server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Check backend health
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Setup frontend
echo "⚛️ Setting up frontend..."
cd ../frontend

# Install frontend dependencies
npm install

# Start frontend
echo "🚀 Starting frontend..."
BROWSER=none npm start &
FRONTEND_PID=$!

echo ""
echo "🎉 Application is starting!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    echo "✅ Servers stopped"
    exit 0
}

trap cleanup INT TERM

# Keep running
wait