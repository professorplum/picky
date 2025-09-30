# Picky - Meal Planner MVP (Local Development)

Simple meal planner with JSON file backend, easily extensible to MongoDB Atlas and Cosmos DB.

## 🏗️ Architecture

```
Local Development:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   HTML/CSS/JS   │────│   Python Flask   │────│   JSON Files    │
│   Frontend      │    │   Server         │    │   (Data Layer)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘

Future Migration Path:
JSON Files → MongoDB Atlas → Cosmos DB
```

## 🚀 Quick Start

### 1. Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

**Alternative: Use the activation script**
```bash
# Make executable and run
chmod +x activate.sh
./activate.sh
```

### 2. Run the App
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Default (port 5001)
python -m backend.run

# Custom port
python -m backend.run --port 8080

# No browser auto-open
python -m backend.run --no-browser

# Both options
python -m backend.run --port 3000 --no-browser
```
This will:
- Start the Flask server on the specified port (default: 5001)
- Automatically open your browser (unless `--no-browser` is used)
- Create a `data/` directory for JSON files

**Note:** Always activate your virtual environment before running the app!

### 3. Start Planning Meals!
- Add meal entries in the weekly grid
- Add/remove persons as needed
- Data auto-saves as you type
- Navigate between weeks

## 📁 Project Structure

```
picky/
├── backend/               # Python Flask application
│   ├── app.py            # Flask server & API routes
│   ├── config.py         # Environment configurations
│   ├── data_layer.py     # JSON file data layer
│   ├── cosmos_data_layer.py  # Cosmos DB data layer
│   └── run.py            # Startup script
├── frontend/              # Static web files
│   ├── index.html        # Main HTML page
│   ├── styles.css        # CSS styles
│   ├── app.js            # Frontend JavaScript
│   ├── logo.png          # Logo image
│   └── favicon.ico       # Favicon
├── tests/                 # Test files
│   ├── test_cosmos_connection.py
│   ├── test_crud_operations.py
│   └── test-cosmos.py
├── scripts/               # Utility scripts
│   ├── data_migration.py # JSON to Cosmos migration
│   ├── schema_migration.py  # Schema management
│   └── reset_cosmos.py   # Database reset utility
├── docs/                  # Documentation
│   ├── architecture.md   # Architecture overview
│   ├── development_workflow.md  # Dev workflow guide
│   ├── COSMOS_SCHEMA.md  # Database schema docs
│   └── SECURITY_FIX_NOTES.md
├── data/                  # JSON data files (auto-created)
├── requirements.txt       # Python dependencies
├── env.example            # Environment variables template
└── README.md              # This file
```

For detailed architecture and workflow documentation, see the [docs/](docs/) directory.

## 🔧 Data Layer Design

The `DataLayer` class provides a clean abstraction that makes it easy to swap backends:

### Current: JSON Files
```python
data_layer = DataLayer()  # Uses JSON files in ./data/
```

### Future: MongoDB Atlas
```python
data_layer = MongoDBDataLayer(connection_string="mongodb+srv://...")
```

### Future: Cosmos DB
```python
data_layer = CosmosDBDataLayer(connection_string="AccountEndpoint=...")
```

## 📊 Data Model

### Meal Data Structure
```json
{
  "local-user": {
    "weekData": {
      "2024-W01": {
        "Monday": {
          "Emma": "Pasta",
          "Jake": "Chicken nuggets"
        },
        "Tuesday": {
          "Emma": "Mac and cheese",
          "Jake": "Pizza"
        }
      }
    },
    "lastUpdated": "2024-01-15T10:30:00Z",
    "userId": "local-user"
  }
}
```

### Person Data Structure
```json
{
  "persons": ["Emma", "Jake", "Sophie", "Alex"],
  "lastUpdated": "2024-01-15T10:30:00Z"
}
```

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/meals/{user_id}` | Get user's meal data |
| POST | `/api/meals/{user_id}` | Save user's meal data |
| PUT | `/api/meals/{user_id}` | Update user's meal data |
| GET | `/api/persons` | Get list of persons |
| POST | `/api/persons` | Add new person |

## 🔄 Migration Path

### Phase 1: Local Development (Current)
- ✅ JSON file backend
- ✅ Local Flask server
- ✅ Simple HTML/CSS/JS frontend

### Phase 2: Cloud Database
- 🔄 MongoDB Atlas integration
- 🔄 Keep same API interface
- 🔄 Same frontend code

### Phase 3: Azure Deployment
- 🔄 Cosmos DB integration
- 🔄 Azure Functions deployment
- 🔄 Static Web Apps hosting

## 🛠️ Development

### Manual Server Start
```bash
python -m backend.app
```

### Using the Development Script
```bash
./run-dev.sh
```

### Frontend Only (if server running elsewhere)
```bash
# Serve HTML files with any HTTP server
python -m http.server 8000
# Then visit http://localhost:8000
```

### Data Directory
The app automatically creates a `data/` directory at the project root with JSON files for local storage.

## 🔒 Security Notes

- Currently designed for local development
- No authentication (single local user)
- Future versions will add proper auth
- Data is stored in plain JSON files

## 🎯 Features

- ✅ Weekly meal planning grid
- ✅ Multiple person support
- ✅ Week navigation
- ✅ Auto-save functionality
- ✅ Add/remove persons
- ✅ Responsive design
- ✅ Clean, extensible architecture

## 🚀 Next Steps

1. **Test locally** - Run the app and plan some meals
2. **Customize** - Modify persons, styling, or features
3. **Extend** - Add new features or data fields
4. **Migrate** - When ready, swap to MongoDB Atlas
5. **Deploy** - Move to Azure with Cosmos DB

## 💡 Benefits of This Approach

- **Fast Development** - Get working app in minutes
- **No Dependencies** - Just Python and a browser
- **Easy Testing** - All data in readable JSON files
- **Extensible** - Clean migration path to cloud
- **Simple** - No complex setup or configuration