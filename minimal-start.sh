#!/bin/bash

echo "🔧 Minimal Finance Analyzer Startup (Core Features Only)"

# Navigate to project directory
cd "$(dirname "$0")"

# Kill any existing processes
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Go to backend
cd backend

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./quick-fix.sh first"
    exit 1
fi

# Remove existing database for fresh start
if [ -f "finance.db" ]; then
    rm finance.db
fi

# Create .env file
cat > .env << 'EOF'
DATABASE_URL=sqlite:///./finance.db
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000
EOF

# Initialize database
echo "🗄️ Creating database..."
python init_sample_data.py

# Start backend with minimal version
echo "🚀 Starting minimal backend server..."
uvicorn app.main_minimal:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait and test backend
sleep 5

if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "⚛️ Starting frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

BROWSER=none npm start &
FRONTEND_PID=$!

echo ""
echo "🎉 Minimal version running!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "⚠️  Note: File import features are disabled in this minimal version"
echo "   Core dashboard and visualization features are available"
echo ""
echo "Press Ctrl+C to stop"

# Cleanup
cleanup() {
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM
wait