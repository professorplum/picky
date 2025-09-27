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

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "OK",
        "message": "Picky API is running",
        "env": app.config.get("ENV_NAME")
    })

@app.route('/api/meals/<user_id>', methods=['GET'])
def get_user_meals(user_id):
    try:
        meals = data_layer.get_user_meals(user_id)
        return jsonify(meals)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meals/<user_id>', methods=['POST'])
def save_user_meals(user_id):
    try:
        data = request.get_json()
        result = data_layer.save_user_meals(user_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meals/<user_id>', methods=['PUT'])
def update_user_meals(user_id):
    try:
        data = request.get_json()
        result = data_layer.update_user_meals(user_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/persons', methods=['GET'])
def get_persons():
    try:
        persons = data_layer.get_persons()
        return jsonify(persons)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/persons', methods=['POST'])
def add_person():
    try:
        data = request.get_json()
        result = data_layer.add_person(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/grocery-items', methods=['GET'])
def get_grocery_items():
    try:
        items = data_layer.get_grocery_items()
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/grocery-items', methods=['POST'])
def save_grocery_items():
    try:
        items = request.get_json()
        result = data_layer.save_grocery_items(items)
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
