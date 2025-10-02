from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
import os

# Import from backend package (works with editable install)
from backend.cosmos_data_layer import CosmosDataLayer
from backend.config import get_config

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

# Initialize Cosmos DB data layer - fail gracefully if configuration is missing
try:
    endpoint = app.config.get('COSMOS_ENDPOINT')
    key = app.config.get('COSMOS_KEY')
    database = app.config.get('COSMOS_DATABASE')
    
    if not endpoint or not key or not database:
        raise ValueError("Cosmos DB configuration missing. Set COSMOS_ENDPOINT, COSMOS_KEY, and COSMOS_DATABASE environment variables.")
    
    data_layer = CosmosDataLayer(endpoint, key, database)
    print(f"Successfully initialized Cosmos DB connection: {database}")
    
except Exception as e:
    print(f"Failed to initialize Cosmos DB: {e}")
    print("App will fail gracefully when attempting to use data layer")
    data_layer = None

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory(str(frontend_dir), 'index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon from frontend directory"""
    return send_from_directory(str(frontend_dir), 'favicon.ico')

@app.route('/api/health', methods=['GET'])
def health():
    config_info = {
        "status": "OK" if data_layer else "ERROR",
        "message": "Picky API is running" if data_layer else "Database connection failed",
        "env": app.config.get("ENV_NAME"),
        "debug": app.config.get("DEBUG"),
        "storage_type": "cosmos_db"
    }
    
    if data_layer:
        config_info["database"] = app.config.get("COSMOS_DATABASE")
        config_info["database_status"] = "connected"
    else:
        config_info["database_status"] = "disconnected"
        config_info["error"] = "Cosmos DB connection not available"
    
    return jsonify(config_info)

def check_data_layer():
    """Helper function to check if data layer is available"""
    if data_layer is None:
        return jsonify({
            "error": "Database connection not available. Please check Cosmos DB configuration.",
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
        items = data_layer.get_larder_items()
        return jsonify(items)
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
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Chopin Liszt (Shopping) ===
@app.route('/api/shopping-items', methods=['GET'])
def get_shopping_items():
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        items = data_layer.get_shopping_items()
        return jsonify(items)
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
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Meals ===
@app.route('/api/meal-items', methods=['GET'])
def get_meal_items():
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        items = data_layer.get_meal_items()
        return jsonify(items)
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
        return jsonify(result)
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
        return jsonify(result)
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
        return jsonify(result)
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
        return jsonify(result)
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
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shopping-items/<item_id>', methods=['DELETE'])
def delete_shopping_item(item_id):
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        result = data_layer.delete_shopping_item(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meal-items/<item_id>', methods=['DELETE'])
def delete_meal_item(item_id):
    error_response = check_data_layer()
    if error_response:
        return error_response
    
    try:
        result = data_layer.delete_meal_item(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_server(port=None, debug=None):
    # Use configuration values if not explicitly provided
    if debug is None:
        debug = app.config.get('DEBUG', True)
    
    # Display startup information
    print("🍽️  Starting Picky...")
    print(f"🌍 Environment: {app.config.get('ENV_NAME', 'Unknown')}")
    
    # Display data storage information
    if data_layer:
        print(f"Data storage: Cosmos DB ({app.config.get('COSMOS_DATABASE', 'picky')})")
    else:
        print("Data storage: ERROR - Cosmos DB connection failed")
    
    print(f"Debug mode: {debug}")
    print(f"Server running at http://localhost:{port}")
    print(f"API available at http://localhost:{port}/api/health")
    
    host = app.config.get('HOST', '0.0.0.0')
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    # Always use PORT env var if set, default to 8000 for Azure compatibility
    port = int(os.environ.get("PORT", 8000))
    run_server(port=port, debug=False)
