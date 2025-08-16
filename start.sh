#!/bin/bash

# Personal Finance Cash Flow Analyzer - Startup Script

echo "🚀 Starting Personal Finance Cash Flow Analyzer..."

# Check if we're in the correct directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/uploads
mkdir -p backend/credentials

# Copy environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
fi

# Initialize backend
echo "🐍 Setting up Python backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize database with sample data
echo "🗄️ Initializing database with sample data..."
python init_sample_data.py

# Start backend server in background
echo "🚀 Starting backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Setup frontend
echo "⚛️ Setting up React frontend..."
cd ../frontend

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install

# Start frontend server
echo "🚀 Starting frontend server..."
npm start &
FRONTEND_PID=$!

# Wait a bit for servers to start
sleep 5

echo ""
echo "✅ Application is starting up!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup INT

# Keep script running
wait