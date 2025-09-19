# Copilot Instructions for Picky Meal Planner

## 🏗️ Architecture Overview
- **Frontend:** `index.html`, `styles.css`, `app.js` (HTML/CSS/JS)
- **Backend:** `app.py` (Flask server), `data_layer.py` (data abstraction)
- **Startup:** `run.py` (main entry point, handles server launch and options)
- **Data Storage:** JSON files in `data/` (`meals.json`, `persons.json`)
- **Extensibility:** Data layer is designed to swap out JSON for MongoDB Atlas or Cosmos DB with minimal code changes.

## 🔑 Key Workflows
- **Local Development:**
  - Activate environment: `source venv/bin/activate` or use `activate.sh`
  - Install dependencies: `pip install -r requirements.txt`
  - Start app: `python run.py` (default port 5001, auto-opens browser)
  - Custom options: `python run.py --port <PORT> --no-browser`
- **Manual server start:** `python app.py` (for direct Flask usage)
- **Frontend-only:** `python -m http.server 8000` (serves static files)

## 🗂️ Data Layer Patterns
- All data access is abstracted via `DataLayer` in `data_layer.py`.
- To migrate to a cloud backend, implement a new class (e.g., `MongoDBDataLayer`) with the same interface.
- Data auto-saves on user actions; no explicit save required in frontend.

## 📊 Data Model Examples
- **Meal data:**
  ```json
  {
    "local-user": {
      "weekData": { "2024-W01": { "Monday": { "Emma": "Pasta" } } },
      "lastUpdated": "2024-01-15T10:30:00Z",
      "userId": "local-user"
    }
  }
  ```
- **Persons data:**
  ```json
  { "persons": ["Emma", "Jake"], "lastUpdated": "2024-01-15T10:30:00Z" }
  ```

## 🌐 API Endpoints
- `GET /api/health` — health check
- `GET/POST/PUT /api/meals/{user_id}` — meal data
- `GET/POST /api/persons` — person list

## 🛠️ Project Conventions
- No authentication; single local user for now
- Data directory is auto-created if missing
- All code is in root except for `data/` JSON files
- Extensible for future cloud migration (see README for migration path)

## 🧩 Integration Points
- Frontend communicates with backend via REST API endpoints
- Data layer is the only backend component that touches persistent storage
- For new features, extend `DataLayer` and update API routes in `app.py`

## 📚 Reference Files
- `README.md` — architecture, setup, data model, migration path
- `data_layer.py` — backend abstraction
- `run.py` — main entry, server options
- `app.py` — Flask routes and API logic
- `data/` — persistent data

---
**For AI agents:**
- Follow the data layer abstraction for any backend changes
- Use provided API endpoints for frontend-backend communication
- Reference `README.md` for setup and migration details
- Keep new code extensible for future cloud backends
