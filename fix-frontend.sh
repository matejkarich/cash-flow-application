#!/bin/bash

echo "🔧 Frontend Fix Script"
echo "====================="

# Navigate to project directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"

# Kill any existing frontend processes
echo "🧹 Stopping any running frontend servers..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Go to frontend directory
cd frontend

echo ""
echo "🗑️ Cleaning up old build files..."
rm -rf node_modules
rm -rf build
rm -f package-lock.json

echo ""
echo "📦 Reinstalling dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ npm install failed"
    exit 1
fi

echo ""
echo "🏗️ Testing build..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "🚀 Starting development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Press Ctrl+C to stop"

# Start the development server
npm start
