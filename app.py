from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from data_layer import DataLayer
from dotenv import load_dotenv
from config import get_config
import os

# Load environment variables from .env file (if it exists)
load_dotenv()

# Create Flask app and configure it
app = Flask(__name__)
config_class = get_config()
app.config.from_object(config_class)

# Configure CORS based on environment
CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))

# Initialize data layer
data_layer = DataLayer()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, etc.) from static/ directory"""
    # Prevent path traversal attacks
    if '..' in filename or filename.startswith('/'):
        return "Access denied", 403
    return send_from_directory('static', filename)

@app.route('/favicon.ico')
def favicon():
    """Serve favicon from root directory"""
    return send_from_directory('.', 'favicon.ico')

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


def run_server(port=None, debug=None):
    # Use configuration values if not explicitly provided
    if debug is None:
        debug = app.config.get('DEBUG', True)
    
    # Display startup information
    print("🍽️  Starting Picky...")
    print(f"🌍 Environment: {app.config.get('ENV_NAME', 'Unknown')}")
    
    # Handle data storage setup based on configuration
    if app.config.get('USE_LOCAL_FILES', True):
        data_dir = app.config.get('DATA_DIR', 'data')
        os.makedirs(data_dir, exist_ok=True)
        print(f"📁 Data storage: Local files in ./{data_dir}/")
    else:
        print(f"🗄️  Data storage: Cosmos DB ({app.config.get('COSMOS_DATABASE', 'picky')})")
    
    print(f"🐛 Debug mode: {debug}")
    print(f"🌐 Server running at http://localhost:{port}")
    print(f"📊 API available at http://localhost:{port}/api/health")
    
    host = app.config.get('HOST', '0.0.0.0')
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    # Always use PORT env var if set, default to 8000 for Azure compatibility
    port = int(os.environ.get("PORT", 8000))
    run_server(port=port, debug=False)
