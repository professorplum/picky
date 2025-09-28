from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from data_layer import DataLayer
import os

app = Flask(__name__)
CORS(app)

# Initialize data layer
data_layer = DataLayer()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, etc.) from static/ directory"""
    return send_from_directory('static', filename)

@app.route('/favicon.ico')
def favicon():
    """Serve favicon from root directory"""
    return send_from_directory('.', 'favicon.ico')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "OK",
        "message": "Picky API is running",
        "env": app.config.get("ENV_NAME")
    })

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
        result = data_layer.add_meal_item(meal_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_server(port=None, debug=True):
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    print("🍽️  Starting Picky...")
    print("📁 Data will be stored in ./data/ directory")
    print(f"🌐 Server running at http://localhost:{port}")
    print(f"📊 API available at http://localhost:{port}/api/health")
    app.run(debug=debug, host='0.0.0.0', port=port)


if __name__ == "__main__":
    # Always use PORT env var if set, default to 8000 for Azure compatibility
    port = int(os.environ.get("PORT", 8000))
    run_server(port=port, debug=False)
