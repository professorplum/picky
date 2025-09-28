#!/bin/bash
# Development server script for Picky Meal Planner
# Uses PORT=8001 to avoid macOS AirPlay Receiver conflict on port 8000

echo "🍽️  Starting Picky development server..."
echo "🌐 Server will be available at http://localhost:8001"
echo "🔧 Development mode with auto-reload enabled"
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  Virtual environment not detected. Run ./activate.sh first!"
    exit 1
fi

# Start the development server with PORT=8001 and debug mode
PORT=8001 python app.py
