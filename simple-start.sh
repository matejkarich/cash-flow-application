#!/bin/bash

echo "🚀 Simple Finance Analyzer Startup"

# Kill any existing processes
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Navigate to project directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"

# Set up backend
echo "🐍 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install simple requirements
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements-simple.txt

# Create simple .env file
echo "📝 Creating .env file..."
cat > .env << 'EOF'
DATABASE_URL=sqlite:///./finance.db
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000
EOF

# Initialize database
echo "🗄️ Setting up database..."
if python init_sample_data.py; then
    echo "✅ Database setup completed"
else
    echo "⚠️ Database setup had issues, but continuing..."
fi

# Start backend
echo "🚀 Starting backend server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Test backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
    echo "📚 API docs at http://localhost:8000/docs"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Set up frontend
echo "⚛️ Setting up frontend..."
cd ../frontend

# Install packages
echo "📦 Installing frontend packages..."
npm install

# Start frontend
echo "🚀 Starting frontend..."
BROWSER=none npm start &
FRONTEND_PID=$!

echo ""
echo "🎉 Servers starting up!"
echo "🌐 Frontend: http://localhost:3000 (may take a minute to start)"
echo "🔗 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"

# Cleanup function
cleanup() {
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM

# Keep running
wait