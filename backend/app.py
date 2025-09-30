from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

# Handle both module execution and direct execution
if __name__ == "__main__" or __package__ is None:
    # Direct execution - add parent dir to path
    sys.path.insert(0, os.path.dirname(__file__))
    from data_layer import DataLayer
    from cosmos_data_layer import CosmosDataLayer
    from config import get_config
else:
    # Module execution
    from .data_layer import DataLayer
    from .cosmos_data_layer import CosmosDataLayer
    from .config import get_config

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

# Initialize data layer based on configuration
use_local_files = app.config.get('USE_LOCAL_FILES')
if use_local_files is None:
    raise ValueError("USE_LOCAL_FILES environment variable must be set to 'true' or 'false'")

# Handle both string and boolean values
if isinstance(use_local_files, bool):
    use_local_files = str(use_local_files).lower()
else:
    use_local_files = str(use_local_files).lower()

if use_local_files in ('true', '1', 'yes', 'on'):
    data_layer = DataLayer()
    print("Using local file storage")
else:
    # Use Cosmos DB - fail if configuration is missing
    endpoint = app.config.get('COSMOS_ENDPOINT')
    key = app.config.get('COSMOS_KEY')
    database = app.config.get('COSMOS_DATABASE')
    
    if not endpoint or not key or not database:
        raise ValueError("Cosmos DB configuration missing. Set COSMOS_ENDPOINT, COSMOS_KEY, and COSMOS_DATABASE environment variables.")
    
    data_layer = CosmosDataLayer(endpoint, key, database)
    print(f"Using Cosmos DB: {database}")

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
        "status": "OK",
        "message": "Picky API is running",
        "env": app.config.get("ENV_NAME"),
        "debug": app.config.get("DEBUG"),
        "storage_type": "local_files" if app.config.get("USE_LOCAL_FILES") else "cosmos_db"
    }
    
    # Only include data_dir for local file storage
    if app.config.get("USE_LOCAL_FILES"):
        config_info["data_dir"] = app.config.get("DATA_DIR")
    else:
        config_info["database"] = app.config.get("COSMOS_DATABASE")
    
    return jsonify(config_info)

# === Larder Liszt (Inventory) ===
@app.route('/api/larder-items', methods=['GET'])
def get_larder_items():
    try:
        items = data_layer.get_larder_items()
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/larder-items', methods=['POST'])
def add_larder_item():
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
    try:
        items = data_layer.get_shopping_items()
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shopping-items', methods=['POST'])
def add_shopping_item():
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
    try:
        items = data_layer.get_meal_items()
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meal-items', methods=['POST'])
def add_meal_item():
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
    try:
        result = data_layer.delete_larder_item(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shopping-items/<item_id>', methods=['DELETE'])
def delete_shopping_item(item_id):
    try:
        result = data_layer.delete_shopping_item(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meal-items/<item_id>', methods=['DELETE'])
def delete_meal_item(item_id):
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
    
    # Handle data storage setup based on configuration
    use_local_files = app.config.get('USE_LOCAL_FILES')
    # Handle both string and boolean values
    if isinstance(use_local_files, bool):
        use_local_files = str(use_local_files).lower()
    else:
        use_local_files = str(use_local_files).lower()
    
    if use_local_files in ('true', '1', 'yes', 'on'):
        data_dir = app.config.get('DATA_DIR', 'data')
        # Ensure data_dir is relative to project root, not backend/
        if not os.path.isabs(data_dir):
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), data_dir)
        os.makedirs(data_dir, exist_ok=True)
        print(f"Data storage: Local files in {data_dir}")
    else:
        print(f"Data storage: Cosmos DB ({app.config.get('COSMOS_DATABASE', 'picky')})")
    
    print(f"Debug mode: {debug}")
    print(f"Server running at http://localhost:{port}")
    print(f"API available at http://localhost:{port}/api/health")
    
    host = app.config.get('HOST', '0.0.0.0')
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    # Always use PORT env var if set, default to 8000 for Azure compatibility
    port = int(os.environ.get("PORT", 8000))
    run_server(port=port, debug=False)
