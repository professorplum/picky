#!/bin/bash
# Development server script for Picky Meal Planner

echo "🍽️  Starting Picky development server for both backend and frontend..."
echo ""

# --- Cleanup function ---
cleanup() {
    echo ""
    echo "🧹 Shutting down servers..."
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID
        echo "Backend server stopped."
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID
        echo "Frontend server stopped."
    fi
    exit 0
}

# Trap SIGINT (Ctrl+C) and call the cleanup function
trap cleanup SIGINT

# --- Virtual Env Check ---
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  Virtual environment not detected. Run ./activate.sh first!"
    exit 1
fi

echo ""

# Create logs directory if it doesn't exist
mkdir -p logs

# --- Start Backend ---
echo "🚀 Starting backend server..."
python run.py --no-browser >> logs/backend.out.log 2>> logs/backend.err.log &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"
echo "🌐 Backend API will be available at http://localhost:${PORT:-8000}"
echo "📝 Backend logs: logs/backend.out.log (stdout) and logs/backend.err.log (stderr)"
echo ""

# --- Start Frontend ---
echo "🚀 Starting frontend development server..."
cd frontend-react
npm run dev >> ../logs/frontend.out.log 2>> ../logs/frontend.err.log &
FRONTEND_PID=$!
cd .. # Return to project root
echo "Frontend server started with PID: $FRONTEND_PID"
echo "🎨 Frontend will be available at http://localhost:5173"
echo "📝 Frontend logs: logs/frontend.out.log (stdout) and logs/frontend.err.log (stderr)"
echo ""

# --- Tail Logs ---
echo "--- 📜 Tailing combined logs (Press Ctrl+C to stop) 📜 ---"
sleep 2 # Give servers a moment to start and create log files
tail -f logs/backend.out.log logs/backend.err.log logs/frontend.out.log logs/frontend.err.log
