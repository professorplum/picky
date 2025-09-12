#!/usr/bin/env python3
"""
Simple startup script for Picky Meal Planner
"""
import os
import sys
import webbrowser
import time
import argparse
from threading import Timer

def main():
    parser = argparse.ArgumentParser(description='Start Picky Meal Planner')
    parser.add_argument('--port', type=int, default=5001, help='Port to run the server on (default: 5001)')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    
    args = parser.parse_args()
    port = args.port
    
    print("🍽️  Picky - Local Development")
    print("=" * 50)
    print("📁 Data will be stored in ./data/ directory")
    if not args.no_browser:
        print(f"🌐 Opening browser at http://localhost:{port}")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Open browser after delay (unless disabled)
    if not args.no_browser:
        Timer(2.0, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    # Start Flask app
    from app import run_server
    run_server(port=port)

if __name__ == '__main__':
    main()
