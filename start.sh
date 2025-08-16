#!/bin/bash

# Personal Finance Cash Flow Analyzer - Startup Script

echo "🚀 Starting Personal Finance Cash Flow Analyzer..."

# Check if we're in the correct directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Store the project root directory
PROJECT_ROOT=$(pwd)

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/uploads
mkdir -p backend/credentials

# Copy environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
echo "🔍 Checking for required tools..."
if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed"
    exit 1
fi

# Initialize backend
echo "🐍 Setting up Python backend..."
cd "$PROJECT_ROOT/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database with sample data
echo "🗄️ Initializing database with sample data..."
if python init_sample_data.py; then
    echo "✅ Database initialized successfully"
else
    echo "❌ Failed to initialize database"
    exit 1
fi

# Start backend server in background
echo "🚀 Starting backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!

# Setup frontend
echo "⚛️ Setting up React frontend..."
cd "$PROJECT_ROOT/frontend"

# Install Node dependencies
echo "Installing Node.js dependencies..."
if npm install; then
    echo "✅ Frontend dependencies installed"
else
    echo "❌ Failed to install frontend dependencies"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend server
echo "🚀 Starting frontend server..."
BROWSER=none npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for servers to start
echo "⏳ Waiting for servers to start..."
sleep 10

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend server is running"
else
    echo "❌ Backend server failed to start. Check backend.log for details."
    kill $FRONTEND_PID 2>/dev/null
    exit 1
fi

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend server is running"
else
    echo "⚠️ Frontend server may still be starting..."
fi

echo ""
echo "🎉 Application is ready!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "📋 Log files:"
echo "   Backend: $PROJECT_ROOT/backend.log"
echo "   Frontend: $PROJECT_ROOT/frontend.log"
echo ""
echo "Press Ctrl+C to stop all servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    
    # Kill any remaining processes on these ports
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup INT TERM

# Keep script running and show the status
while true; do
    sleep 30
    
    # Check if processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend server has stopped unexpectedly"
        break
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ Frontend server has stopped unexpectedly"
        break
    fi
done

cleanup