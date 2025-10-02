# Picky - Meal Planner MVP

Simple meal planner with Azure Cosmos DB backend for scalable cloud storage.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   HTML/CSS/JS   │────│   Python Flask   │────│   Azure Cosmos  │
│   Frontend      │    │   Server         │    │   DB (Cloud)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Current Features:**
- **Larder Liszt**: Track pantry items and reorder status
- **Chopin Liszt**: Shopping list with cart status
- **Meals**: Meal planning with ingredients

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


### 2. Configure Azure Key Vault
The app uses Azure Key Vault for secure credential management. You need:

1. **Set up Azure authentication:**
   ```bash
   az login
   ```

2. **Configure Key Vault URL in your `.env` file:**
   ```bash
   KEY_VAULT_URL="https://your-keyvault.vault.azure.net/"
   ```

3. **The app will automatically fetch Cosmos DB connection string from Key Vault**

### 3. Run the App
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Default (port 5001)
python -m backend.run

# Custom port
python -m backend.run --port 8080

# No browser auto-open
python -m backend.run --no-browser

# Development script (uses port 8001)
./run-dev.sh

# Alternative: Direct Flask app (uses PORT env var or defaults to 8000)
python -m backend.app
```

**Note:** Always activate your virtual environment before running the app!

### 4. Start Using Picky!
- **Larder Liszt**: Add pantry items, mark for reorder
- **Chopin Liszt**: Add shopping items, mark as in cart
- **Meals**: Add meal ideas with ingredients
- Data auto-saves as you type

## 📁 Project Structure

```
picky/
├── backend/               # Python Flask application
│   ├── app.py            # Flask server & API routes
│   ├── config.py         # Environment configurations
│   ├── database_service.py # Cosmos DB connection service
│   ├── data_layer.py     # Data access layer
│   ├── secrets_service.py # Azure Key Vault integration
│   └── run.py            # Startup script
├── frontend/              # Static web files
│   ├── index.html        # Main HTML page
│   ├── styles.css        # CSS styles
│   ├── app.js            # Frontend JavaScript
│   ├── logo.png          # Logo image
│   └── favicon.ico       # Favicon
├── tests/                 # Test files
│   ├── test_api_endpoints.py
│   ├── test_crud_operations.py
│   ├── test_data_layer_crud.py
│   └── test_cosmos_connection.py
├── scripts/               # Utility scripts
│   └── reset_cosmos.py   # Database reset utility
├── docs/                  # Documentation
│   ├── architecture.md   # Architecture overview
│   ├── development_workflow.md  # Dev workflow guide
│   ├── COSMOS_SCHEMA.md  # Database schema docs
│   └── SECURITY_FIX_NOTES.md
├── .env                    # Environment configuration (create from env.example)
├── requirements.txt       # Python dependencies
├── env.example            # Environment variables template
└── README.md              # This file
```

For detailed architecture and workflow documentation, see the [docs/](docs/) directory.

## 🔧 Data Layer Design

The `DataLayer` class provides a clean abstraction with Azure Key Vault integration:

### Current: Azure Cosmos DB with Key Vault
```python
# Uses Azure Key Vault for secure credential management
data_layer = DataLayer()  # Automatically connects via Key Vault
```

The app uses:
- **DatabaseService**: Manages Cosmos DB connections with health checks
- **SecretsService**: Retrieves credentials from Azure Key Vault
- **DataLayer**: Provides clean CRUD interface for all item types

## 📊 Data Model

### Larder Items
```json
{
  "id": "1759017526823-4567",
  "name": "bananas",
  "type": "larder",
  "reorder": false,
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071"
}
```

### Shopping Items
```json
{
  "id": "1759017526823-4567",
  "name": "milk",
  "type": "shopping",
  "inCart": false,
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071"
}
```

### Meal Items
```json
{
  "id": "1759016375267-8901",
  "name": "Chicken Stir Fry",
  "type": "meal",
  "ingredients": "chicken, vegetables, soy sauce",
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071"
}
```

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/larder-items` | Get all larder items |
| POST | `/api/larder-items` | Add new larder item |
| PUT | `/api/larder-items/{id}` | Update larder item |
| DELETE | `/api/larder-items/{id}` | Delete larder item |
| GET | `/api/shopping-items` | Get all shopping items |
| POST | `/api/shopping-items` | Add new shopping item |
| PUT | `/api/shopping-items/{id}` | Update shopping item |
| DELETE | `/api/shopping-items/{id}` | Delete shopping item |
| GET | `/api/meal-items` | Get all meal items |
| POST | `/api/meal-items` | Add new meal item |
| PUT | `/api/meal-items/{id}` | Update meal item |
| DELETE | `/api/meal-items/{id}` | Delete meal item |

## 🔄 Current State

### Phase 1: Local Development (Current)
- ✅ Azure Cosmos DB backend with Key Vault
- ✅ Local Flask server
- ✅ Simple HTML/CSS/JS frontend
- ✅ Three item types: larder, shopping, meals

### Phase 2: Azure Deployment (Planned)
- 🔄 Azure App Service deployment
- 🔄 Azure Application Insights monitoring
- 🔄 GitHub Actions CI/CD pipeline

## 🛠️ Development

### Server Options
```bash
# Recommended: Use the startup script (port 5001)
python -m backend.run

# Development script (port 8001)
./run-dev.sh

# Direct Flask app (uses PORT env var or defaults to 8000)
python -m backend.app
```

### Environment Configuration
The app uses Azure Key Vault for secure credential management. Copy `env.example` to `.env` and set your Key Vault URL. The app will automatically fetch Cosmos DB credentials from Key Vault.

**Note:** The current `env.example` uses `ENV=dev` but the code expects `ENV_NAME` with values like `Development`. This will be aligned in a future update.

## 🔒 Security Notes

- Currently designed for local development
- No authentication (single local user)
- Credentials managed via Azure Key Vault
- Data is stored in Azure Cosmos DB
- Future versions will add proper auth

## 🎯 Features

- ✅ Larder Liszt: Track pantry items and reorder status
- ✅ Chopin Liszt: Shopping list with cart status
- ✅ Meals: Meal planning with ingredients
- ✅ Auto-save functionality
- ✅ Responsive design
- ✅ Clean, extensible architecture

## 🚀 Next Steps

1. **Test locally** - Run the app and try all three item types
2. **Customize** - Modify styling or add features
3. **Extend** - Add new features or data fields
4. **Deploy** - Move to Azure App Service with Application Insights

## 💡 Benefits of This Approach

- **Fast Development** - Get working app in minutes
- **Secure** - Azure Key Vault for credential management
- **Cloud Storage** - Scalable Azure Cosmos DB backend
- **Extensible** - Clean architecture for future features
- **Simple** - Minimal setup with Azure authentication