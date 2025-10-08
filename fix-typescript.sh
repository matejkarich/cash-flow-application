#!/bin/bash

echo "🔧 TypeScript Configuration Fix"
echo "==============================="

# Navigate to project directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"

# Go to frontend directory
cd frontend

echo ""
echo "📋 Current frontend structure:"
ls -la src/

echo ""
echo "🔍 Checking for TypeScript config..."
if [ -f "tsconfig.json" ]; then
    echo "✅ tsconfig.json exists"
    cat tsconfig.json
else
    echo "❌ tsconfig.json missing - this is likely the issue!"
fi

echo ""
echo "🔍 Checking App.tsx file..."
if [ -f "src/App.tsx" ]; then
    echo "✅ App.tsx exists"
    echo "First few lines:"
    head -5 src/App.tsx
else
    echo "❌ App.tsx missing!"
fi

echo ""
echo "🔍 Checking index.tsx file..."
if [ -f "src/index.tsx" ]; then
    echo "✅ index.tsx exists"
    echo "Content:"
    cat src/index.tsx
else
    echo "❌ index.tsx missing!"
fi

echo ""
echo "🧹 Cleaning up and reinstalling..."
rm -rf node_modules
rm -f package-lock.json

echo "📦 Installing dependencies..."
npm install

echo ""
echo "🏗️ Testing TypeScript compilation..."
npx tsc --noEmit

if [ $? -eq 0 ]; then
    echo "✅ TypeScript compilation successful!"
else
    echo "❌ TypeScript compilation failed"
    echo "Trying to build anyway..."
fi

echo ""
echo "🚀 Starting development server..."
echo "If you see errors, they should be more specific now."
echo "Frontend will be at: http://localhost:3000"

npm start
