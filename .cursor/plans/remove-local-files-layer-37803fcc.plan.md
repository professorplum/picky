<!-- 37803fcc-a08e-4c4d-a832-58223d5b8be9 5f599b9c-06f6-41bb-a0db-06d36365b53f -->
# Remove Local File Data Layer - Cosmos DB Only

## Overview

Remove local file data storage completely and simplify the application to use only Cosmos DB across all environments (dev, stage, prod). This eliminates environment inconsistencies and simplifies the codebase.

---

## Portal Steps (You'll Do These)

### 1. Create Free Tier Cosmos DB Account in Azure Portal

1. **Navigate to Azure Portal**: Go to [https://portal.azure.com](https://portal.azure.com)

2. **Create Resource Group** (if you don't have one):

- Click "Resource groups" → "Create"
- Name: `picky-dev-rg` (or your preferred name)
- Region: Choose closest to you (e.g., `East US`, `West Europe`)
- Click "Review + create" → "Create"

3. **Create Cosmos DB Account**:

- Click "Create a resource" → Search "Azure Cosmos DB" → "Create"
- **Basics tab**:
- Subscription: Your Azure subscription
- Resource Group: Select the one you created
- Account Name: `picky-dev-cosmos` (must be globally unique)
- Location: Same as your resource group
- Capacity mode: **Provisioned throughput**
- **Apply Free Tier Discount**: ✅ **Apply** (CRITICAL - this enables free tier)
- API: **Azure Cosmos DB for NoSQL** (default, already what you're using)
- **Global Distribution tab**: Leave defaults (single region is fine for dev)
- **Networking tab**: Leave defaults (allow public access for dev)
- **Backup Policy tab**: Leave defaults
- **Encryption tab**: Leave defaults
- Click "Review + create" → "Create"
- Wait for deployment (~3-5 minutes)

4. **Create Database and Containers**:

- Once deployed, click "Go to resource"
- In left menu, click "Data Explorer"
- Click "New Database"
- Database id: `picky-dev`
- **Share throughput across containers**: ✅ Check this box
- Throughput: Set to **1000 RU/s (Manual)** (uses your free tier)
- Click "OK"
- The containers (`shopping_items`, `larder_items`, `meal_items`) will be auto-created by your app on first run

5. **Get Connection Credentials**:

- In left menu, click "Keys"
- Copy these values (you'll need them for `.env`):
- **URI** (e.g., `https://picky-dev-cosmos.documents.azure.com:443/`)
- **PRIMARY KEY** (long string)
- Database name: `picky-dev`

---

## Code Changes (I'll Do These)

### Remove local file data layer

- Delete `/workspaces/picky/backend/data_layer.py`
- Remove `USE_LOCAL_FILES` and `DATA_DIR` config variables from `backend/config.py`
- Simplify `backend/app.py` to always use `CosmosDataLayer` (remove conditional logic)
- Update `backend/config.py` to always require Cosmos DB credentials

### Update configuration

- Remove local file references from `env.example`
- Update all three config classes (Development, Staging, Production) to require Cosmos credentials
- Remove `USE_LOCAL_FILES` logic entirely

### Update documentation

- Update `README.md` to remove local file storage references
- Update `docs/architecture.md` to reflect Cosmos-only approach
- Update `.github/copilot-instructions.md` to remove data layer switching info

### Clean up references

- Update `tests/test-cosmos.py` to remove local files option
- Remove any references to the `data/` directory for storage (keep only for migrations if needed)

---

## Testing Steps (We'll Do Together After You Create Cosmos DB)

1. You provide the Cosmos DB credentials from Azure Portal
2. Update `.env` file in Codespace with your dev Cosmos credentials
3. Test app startup and verify connection to dev Cosmos DB
4. Test CRUD operations (create, read, update, delete) for all three data types
5. Verify `/api/health` endpoint shows correct Cosmos DB configuration

---

## Notes

- **Free Tier**: Staying under 1000 RU/s and 25 GB = $0 cost
- **Shared Throughput**: Database-level provisioning shares 1000 RU/s across all containers
- **No MongoDB**: Sticking with NoSQL (SQL) API - what you're already using
- **Environment Consistency**: Same code path for dev → stage → prod, only credentials differ