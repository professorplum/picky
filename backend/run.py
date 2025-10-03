#!/usr/bin/env python3
"""
Simple startup script for Picky Meal Planner
"""
import os
import sys
import webbrowser
import time
import argparse
import logging
from threading import Timer

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Start Picky Meal Planner')
    parser.add_argument('--port', type=int, help='Port to run the server on')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')

    args = parser.parse_args()

    # Best practice: PORT env var > --port argument > default
    port_env = os.environ.get('PORT')
    if port_env:
        port = int(port_env)
    elif args.port:
        port = args.port
    else:
        port = 8000

    # Only show startup messages in development
    env = os.environ.get('ENV', 'dev')
    if env == 'dev':
        logger.info("Picky - Meal Planner")
        logger.info("=" * 50)
        logger.info("Data will be stored in Azure Cosmos DB")
        logger.info(f"Effective port: {port}")
        if not args.no_browser:
            logger.info(f"Opening browser at http://localhost:{port}")
        logger.info("Press Ctrl+C to stop the server")
        logger.info("=" * 50)

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
        logger.error(f"Error starting server: {e}")
        if not args.no_browser:
            logger.warning("Browser opening cancelled due to server error.")

if __name__ == '__main__':
    main()
