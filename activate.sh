#!/bin/bash
# Activation script for Picky Meal Planner (Unix/Linux/macOS and Git-Bash on Windows)

echo "🍽️  Activating Picky Meal Planner environment..."
source venv/bin/activate
echo "✅ Virtual environment activated!"

echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Check requirements.txt"
    exit 1
fi

echo "📦 Installed packages:"
pip list | grep -E "(flask|cors|dotenv)"
echo ""
echo "🚀 To start the app for development, run: ./run-dev.sh"
echo "🚀 To start the app normally, run: python app.py"
echo "🛑 To deactivate, run: deactivate"
