#!/bin/bash
# Development server script for Picky Meal Planner

echo "🍽️  Starting Picky development server..."
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  Virtual environment not detected. Run ./activate.sh first!"
    exit 1
fi

echo ""
echo "🌐 Server will be available at http://localhost:${PORT:-8000}"
echo "🔧 Development mode: DEBUG=${DEBUG:-true} (auto-reload enabled)"
echo ""

# Start the development server via run.py (proper entry point)
python -m backend.run --no-browser
