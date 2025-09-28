# Copilot Instructions for Picky Meal Planner

## 🏗️ Architecture Overview
- **Frontend:** `index.html`, `styles.css`, `app.js` (vanilla HTML/CSS/JS, no framework)
- **Backend:** `app.py` (Flask API server), `data_layer.py` (data abstraction)
- **Startup:** `run.py` (main entry, handles server launch, port, browser options)
- **Data Storage:** JSON files in `data/` (e.g., `meals.json`, `persons.json`, `grocery_items.json`)
- **Extensibility:** Data layer is designed for easy migration to cloud DBs (MongoDB, Cosmos DB) by subclassing `DataLayer`.

## 🔑 Key Developer Workflows
- **Local dev:**
  - Activate env: `activate.sh` (bash) or `activate.bat` (Windows)
  - Install deps: `pip install -r requirements.txt`
  - Start app: `python run.py` (default port 5001, auto-opens browser)
  - Custom: `python run.py --port <PORT> --no-browser`
- **Direct Flask:** `python app.py` (for debugging Flask only)
- **Frontend-only:** `python -m http.server 8000` (serves static files, no backend)

## 🗂️ Data Layer Patterns
- All persistent data access is via `DataLayer` in `data_layer.py`.
- To swap storage, subclass `DataLayer` and update backend wiring in `app.py`.
- Data auto-saves on user actions; frontend does not manage persistence.

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
- `GET|POST|PUT /api/meals/{user_id}` — meal data
- `GET|POST /api/persons` — person list

## 🛠️ Project Conventions
- No authentication; single local user only
- `data/` is auto-created if missing
- All code in root except for `data/` and `static/`
- Extensible for future cloud migration (see `README.md`)

## 🧩 Integration Points
- Frontend uses REST API endpoints in `app.py` for all data
- Only `data_layer.py` touches persistent storage
- For new features: extend `DataLayer`, update API routes in `app.py`, and update frontend API calls

## 📚 Reference Files
- `README.md` — architecture, setup, data model, migration path
- `data_layer.py` — backend data abstraction
- `run.py` — main entry, server options
- `app.py` — Flask routes and API logic
- `data/` — persistent data

---
**For AI agents:**
- Always use the data layer abstraction for backend changes
- Use REST API endpoints for frontend-backend communication
- Reference `README.md` for setup, data model, and migration details
- Keep new code extensible for future cloud backends
