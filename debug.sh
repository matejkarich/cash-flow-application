#!/bin/bash

echo "🔍 Finance Analyzer Debug Information"
echo "=================================="

# Check current directory
echo "📁 Current directory: $(pwd)"
echo "📁 Directory contents:"
ls -la

echo ""
echo "🐍 Python Information:"
echo "Python version: $(python3 --version)"
echo "Python location: $(which python3)"

echo ""
echo "📦 Node.js Information:"
echo "Node version: $(node --version 2>/dev/null || echo 'Not found')"
echo "npm version: $(npm --version 2>/dev/null || echo 'Not found')"

echo ""
echo "🗂️ Project Structure:"
echo "Backend exists: $([ -d 'backend' ] && echo 'Yes' || echo 'No')"
echo "Frontend exists: $([ -d 'frontend' ] && echo 'Yes' || echo 'No')"
echo "README exists: $([ -f 'README.md' ] && echo 'Yes' || echo 'No')"

if [ -d "backend" ]; then
    echo ""
    echo "🐍 Backend Status:"
    echo "Virtual env exists: $([ -d 'backend/venv' ] && echo 'Yes' || echo 'No')"
    echo "Requirements file: $([ -f 'backend/requirements.txt' ] && echo 'Yes' || echo 'No')"
    echo "Simple requirements: $([ -f 'backend/requirements-simple.txt' ] && echo 'Yes' || echo 'No')"
    echo "Main app file: $([ -f 'backend/app/main.py' ] && echo 'Yes' || echo 'No')"
    echo "Database init: $([ -f 'backend/init_sample_data.py' ] && echo 'Yes' || echo 'No')"
fi

if [ -d "frontend" ]; then
    echo ""
    echo "⚛️ Frontend Status:"
    echo "Package.json exists: $([ -f 'frontend/package.json' ] && echo 'Yes' || echo 'No')"
    echo "Public/index.html: $([ -f 'frontend/public/index.html' ] && echo 'Yes' || echo 'No')"
    echo "src/index.tsx: $([ -f 'frontend/src/index.tsx' ] && echo 'Yes' || echo 'No')"
    echo "src/App.tsx: $([ -f 'frontend/src/App.tsx' ] && echo 'Yes' || echo 'No')"
    echo "node_modules: $([ -d 'frontend/node_modules' ] && echo 'Yes' || echo 'No')"
fi

echo ""
echo "🌐 Port Status:"
echo "Port 8000 in use: $(lsof -ti:8000 > /dev/null && echo 'Yes' || echo 'No')"
echo "Port 3000 in use: $(lsof -ti:3000 > /dev/null && echo 'Yes' || echo 'No')"

if lsof -ti:8000 > /dev/null; then
    echo "Process on 8000: $(lsof -ti:8000 | head -1 | xargs ps -p | tail -1)"
fi

if lsof -ti:3000 > /dev/null; then
    echo "Process on 3000: $(lsof -ti:3000 | head -1 | xargs ps -p | tail -1)"
fi

echo ""
echo "🩺 Quick Health Check:"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend responding at http://localhost:8000"
    echo "Health response: $(curl -s http://localhost:8000/health)"
else
    echo "❌ Backend not responding at http://localhost:8000"
fi

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend responding at http://localhost:3000"
else
    echo "❌ Frontend not responding at http://localhost:3000"
fi

echo ""
echo "🔧 Recommended Actions:"
echo "1. Run './simple-start.sh' for a clean setup"
echo "2. Check log files: backend.log and frontend.log (if they exist)"
echo "3. Make sure Python 3.9+ and Node.js 16+ are installed"