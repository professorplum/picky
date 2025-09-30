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
    parser.add_argument('--port', type=int, help='Port to run the server on')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')

    args = parser.parse_args()

    # Best practice: --port argument > PORT env var > default
    port = args.port
    if port is None:
        port_env = os.environ.get('PORT')
        if port_env:
            port = int(port_env)
        else:
            port = 5001

    print("Picky - Local Development")
    print("=" * 50)
    print("Data will be stored in ./data/ directory")
    print(f"Effective port: {port}")
    if not args.no_browser:
        print(f"Opening browser at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)

    # Open browser after delay (unless disabled)
    if not args.no_browser:
        Timer(2.0, lambda: webbrowser.open(f'http://localhost:{port}')).start()

    # Start Flask app
    try:
        # Handle both module execution and direct execution
        try:
            from .app import run_server
        except ImportError:
            from app import run_server
        run_server(port=port, debug=False)
    except Exception as e:
        print(f"Error starting server: {e}")
        if not args.no_browser:
            print("Browser opening cancelled due to server error.")

if __name__ == '__main__':
    main()
