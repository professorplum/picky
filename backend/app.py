from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)

# Import from backend package (works with editable install)
from backend.config import get_config
from backend.database_service import get_database_service, initialize_database
from backend.data_layer import DataLayer

# Load environment variables from .env file (if it exists)
load_dotenv()

# Determine paths for Flask app using pathlib for robust path handling
# Frontend directory is one level up from backend, then into frontend/
backend_dir = Path(__file__).resolve().parent
project_root = backend_dir.parent
frontend_dir = project_root / 'frontend'

# Create Flask app with frontend as both template and static folder
app = Flask(__name__, 
            static_folder=str(frontend_dir),
            static_url_path='/static',
            template_folder=str(frontend_dir))
config_class = get_config()
app.config.from_object(config_class)

# Configure CORS based on environment
CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))

# Initialize database service with new architecture
try:
    # Initialize the new database service
    db_connected = initialize_database()
    if db_connected:
        if app.config.get('ENV') == 'dev':
            logger.info("Successfully initialized Cosmos DB connection with new architecture")
        
        # Initialize the new data layer
        data_layer = DataLayer()
        if app.config.get('ENV') == 'dev':
            logger.info("Successfully initialized new data layer")
    else:
        logger.error("Failed to initialize Cosmos DB connection")
        data_layer = None
    
except Exception as e:
    logger.error(f"SHOWSTOPPER: Failed to initialize database service: {e}")
    logger.error("SHOWSTOPPER: Cannot start application without database connection")
    logger.error("SHOWSTOPPER: Exiting to prevent serving broken application")
    import sys
    sys.exit(1)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory(str(frontend_dir), 'index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint for database connection"""
    try:
        db_service = get_database_service()
        health_status = db_service.get_health_status()
        
        if health_status['connected']:
            return jsonify({
                "status": "healthy",
                "database": health_status,
                "message": "Database connection is healthy"
            }), 200
        else:
            return jsonify({
                "status": "unhealthy", 
                "database": health_status,
                "message": f"Database connection failed: {health_status.get('error', 'Unknown error')}"
            }), 503
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Health check failed: {str(e)}"
        }), 500

@app.route('/favicon.ico')
def favicon():
    """Serve favicon from frontend directory"""
    return send_from_directory(str(frontend_dir), 'favicon.ico')


def check_data_layer():
    """Helper function to check if data layer is available"""
    if data_layer is None:
        return jsonify({
            "error": "Database connection not available. Please check Cosmos DB configuration.",
            "status": "database_error"
        }), 503
    
    # Check if data layer is connected
    if not data_layer.db_service.is_connected():
        return jsonify({
            "error": "Database connection lost",
            "status": "database_error"
        }), 503
    return None

# === Larder Liszt (Inventory) ===
@app.route('/api/larder-items', methods=['GET'])
def get_larder_items():
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        result = data_layer.get_larder_items()
        if result.get("success"):
            return jsonify(result["items"])
        else:
            return jsonify({"error": result.get("error", "Failed to get larder items")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/larder-items', methods=['POST'])
def add_larder_item():
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        item_data = request.get_json()
        if not item_data or not isinstance(item_data, dict):
            return jsonify({"error": "Invalid JSON data"}), 400
        
        # Validate required fields
        if 'name' not in item_data or not item_data['name'].strip():
            return jsonify({"error": "Item name is required"}), 400
        
        result = data_layer.add_larder_item(item_data)
        if result.get("success"):
            return jsonify(result["item"])
        else:
            return jsonify({"error": result.get("error", "Failed to add larder item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Chopin Liszt (Shopping) ===
@app.route('/api/shopping-items', methods=['GET'])
def get_shopping_items():
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        result = data_layer.get_shopping_items()
        if result.get("success"):
            return jsonify(result["items"])
        else:
            return jsonify({"error": result.get("error", "Failed to get shopping items")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shopping-items', methods=['POST'])
def add_shopping_item():
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        item_data = request.get_json()
        if not item_data or not isinstance(item_data, dict):
            return jsonify({"error": "Invalid JSON data"}), 400
        
        # Validate required fields
        if 'name' not in item_data or not item_data['name'].strip():
            return jsonify({"error": "Item name is required"}), 400
        
        result = data_layer.add_shopping_item(item_data)
        if result.get("success"):
            return jsonify(result["item"])
        else:
            return jsonify({"error": result.get("error", "Failed to add shopping item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Meals ===
@app.route('/api/meal-items', methods=['GET'])
def get_meal_items():
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        result = data_layer.get_meal_items()
        if result.get("success"):
            return jsonify(result["items"])
        else:
            return jsonify({"error": result.get("error", "Failed to get meal items")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meal-items', methods=['POST'])
def add_meal_item():
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        meal_data = request.get_json()
        if not meal_data or not isinstance(meal_data, dict):
            return jsonify({"error": "Invalid JSON data"}), 400
        
        # Validate required fields
        if 'name' not in meal_data or not meal_data['name'].strip():
            return jsonify({"error": "Meal name is required"}), 400
        
        result = data_layer.add_meal_item(meal_data)
        if result.get("success"):
            return jsonify(result["item"])
        else:
            return jsonify({"error": result.get("error", "Failed to add meal item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Update Operations ===
@app.route('/api/larder-items/<item_id>', methods=['PUT'])
def update_larder_item(item_id):
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        update_data = request.get_json()
        if not update_data or not isinstance(update_data, dict):
            return jsonify({"error": "Invalid JSON data"}), 400
        
        result = data_layer.update_larder_item(item_id, update_data)
        if result.get("success"):
            return jsonify(result["item"])
        else:
            return jsonify({"error": result.get("error", "Failed to update larder item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shopping-items/<item_id>', methods=['PUT'])
def update_shopping_item(item_id):
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        update_data = request.get_json()
        if not update_data or not isinstance(update_data, dict):
            return jsonify({"error": "Invalid JSON data"}), 400
        
        result = data_layer.update_shopping_item(item_id, update_data)
        if result.get("success"):
            return jsonify(result["item"])
        else:
            return jsonify({"error": result.get("error", "Failed to update shopping item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meal-items/<item_id>', methods=['PUT'])
def update_meal_item(item_id):
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        update_data = request.get_json()
        if not update_data or not isinstance(update_data, dict):
            return jsonify({"error": "Invalid JSON data"}), 400
        
        result = data_layer.update_meal_item(item_id, update_data)
        if result.get("success"):
            return jsonify(result["item"])
        else:
            return jsonify({"error": result.get("error", "Failed to update meal item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Delete Operations ===
@app.route('/api/larder-items/<item_id>', methods=['DELETE'])
def delete_larder_item(item_id):
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        result = data_layer.delete_larder_item(item_id)
        if result.get("success"):
            return jsonify({"message": result.get("message", "Larder item deleted successfully")})
        else:
            return jsonify({"error": result.get("error", "Failed to delete larder item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shopping-items/<item_id>', methods=['DELETE'])
def delete_shopping_item(item_id):
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        result = data_layer.delete_shopping_item(item_id)
        if result.get("success"):
            return jsonify({"message": result.get("message", "Shopping item deleted successfully")})
        else:
            return jsonify({"error": result.get("error", "Failed to delete shopping item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meal-items/<item_id>', methods=['DELETE'])
def delete_meal_item(item_id):
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        result = data_layer.delete_meal_item(item_id)
        if result.get("success"):
            return jsonify({"message": result.get("message", "Meal item deleted successfully")})
        else:
            return jsonify({"error": result.get("error", "Failed to delete meal item")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_server(port=None, debug=None):
    # Use configuration values if not explicitly provided
    if debug is None:
        debug = app.config.get('DEBUG', True)
    
    # Display startup information (only in development)
    if app.config.get('ENV') == 'dev':
        logger.info("🍽️  Starting Picky...")
        logger.info(f"🌍 Environment: {app.config.get('ENV', 'Unknown')}")
        
        # Display data storage information
        if data_layer:
            logger.info(f"Data storage: Cosmos DB ({app.config.get('COSMOS_DATABASE', 'picky')})")
        else:
            logger.warning("Data storage: ERROR - Cosmos DB connection failed")
        
        logger.info(f"Debug mode: {debug}")
        logger.info(f"Server running at http://localhost:{port}")
        logger.info(f"API available at http://localhost:{port}/api/health")
    
    host = app.config.get('HOST', '0.0.0.0')
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    # Always use PORT env var if set, default to 8000 for Azure compatibility
    port = int(os.environ.get("PORT", 8000))
    run_server(port=port, debug=False)
