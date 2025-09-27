#!/bin/bash
# Activation script for Picky Meal Planner (Unix/Linux/macOS and Git-Bash on Windows)

echo "🍽️  Activating Picky Meal Planner environment..."
source venv/bin/activate
echo "✅ Virtual environment activated!"
echo "📦 Installed packages:"
pip list | grep -E "(flask|cors|dotenv)"
echo ""
echo "🚀 To start the app, run: python run.py"
echo "🛑 To deactivate, run: deactivate"
