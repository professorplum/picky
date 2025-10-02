# Cosmos DB Schema Design for Picky Meal Planner

## Overview

This document describes the Cosmos DB schema design for the Picky application, including container structure and document formats.

## Container Design

The application uses a **single container** with **flexible `/id` partition key** for maximum adaptability and future schema evolution. Items are differentiated by a `type` field within the same container.

### Container Configuration

| Container Name | Purpose | Partition Key | Throughput |
|----------------|---------|---------------|------------|
| `dev-container` | Development environment data | `/id` | 1000 RU/s |
| `stage-container` | Staging environment data | `/id` | 1000 RU/s |
| `prod-container` | Production environment data | `/id` | 1000 RU/s |

**Note**: Container names are environment-derived based on the Azure Key Vault configuration. Each environment uses its own container for data isolation.

## Document Schemas

### Shopping Items (Shopping List)

**Container:** Single container (type: `shopping`)

```json
{
  "id": "1759017526823-4567",
  "name": "bananas",
  "type": "shopping",
  "inCart": false,
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071"
}
```

**Fields:**
- `id` (string, required): Unique identifier (timestamp-random)
- `name` (string, required): Item name
- `type` (string, required): Item type (`"shopping"`)
- `inCart` (boolean): Whether item is in shopping cart
- `createdAt` (string): ISO timestamp when created
- `modifiedAt` (string): ISO timestamp when last modified

### Larder Items (Larder/Pantry)

**Container:** Single container (type: `larder`)

```json
{
  "id": "1759016375267-8901",
  "name": "apples",
  "type": "larder",
  "reorder": false,
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071"
}
```

**Fields:**
- `id` (string, required): Unique identifier
- `name` (string, required): Item name
- `type` (string, required): Item type (`"larder"`)
- `reorder` (boolean): Whether item needs reordering
- `createdAt` (string): ISO timestamp when created
- `modifiedAt` (string): ISO timestamp when last modified

### Meal Items

**Container:** Single container (type: `meal`)

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

**Fields:**
- `id` (string, required): Unique identifier
- `name` (string, required): Meal name
- `type` (string, required): Item type (`"meal"`)
- `ingredients` (string): List of ingredients
- `createdAt` (string): ISO timestamp when created
- `modifiedAt` (string): ISO timestamp when last modified

## Query Patterns

Since all items are stored in a single container, queries use the `type` field to filter items:

```sql
-- Get all shopping items
SELECT * FROM c WHERE c.type = "shopping"

-- Get all larder items
SELECT * FROM c WHERE c.type = "larder"

-- Get all meal items
SELECT * FROM c WHERE c.type = "meal"
```

## ID Generation Strategy

### New Documents
- **Format:** `{timestamp}-{random}`
- **Example:** `1759121118216-3947`
- **Implementation:** `int(datetime.utcnow().timestamp() * 1000)` + 4-digit random suffix

### Migrated Documents
- **Grocery/Inventory Items:** Convert original numeric ID to string
- **Persons:** Generate sequential IDs (`person-1`, `person-2`, etc.)
- **Preserve original IDs** in `originalId` field for reference

## Metadata Handling

### Cosmos DB Internal Fields (Filtered Out)
- `_rid`: Resource ID (internal)
- `_self`: Self-link (internal)
- `_etag`: Entity tag for concurrency (internal)
- `_attachments`: Attachments link (internal)
- `_ts`: Timestamp (internal)
- `ttl`: Time-to-live (if used)

### Application Fields
- `createdAt`: Application-controlled creation timestamp

## Schema Evolution

### Easy Changes (No Migration Required)
- ✅ Add new fields to documents
- ✅ Remove fields (stop writing them)
- ✅ Change field types (with validation)
- ✅ Add new containers
- ✅ Modify throughput settings

### Complex Changes (Requires Data Movement)
- ⚠️ Change partition key (create new container, move data)
- ⚠️ Rename containers (create new, move data, delete old)
- ⚠️ Major schema restructuring

### Best Practices
- **Version documents** if needed (`schemaVersion: "1.0"`)
- **Use optional fields** for new features
- **Maintain backward compatibility** during transitions
- **Test schema changes** in development first

## Performance Considerations

### Partition Key Strategy
- **Using `/id`** provides maximum flexibility
- **Even distribution** across partitions (timestamp-based IDs)
- **No hot partitions** expected with current usage patterns

### Query Patterns
- **Point reads** by ID (most efficient)
- **Cross-partition queries** for listing all items (acceptable for small datasets)
- **Future optimization** possible with different partition strategies if needed

### Throughput Planning
- **Free Tier:** 1000 RU/s shared across all containers in the database
- **Database-level throughput:** All containers share the 1000 RU/s allocation
- **Cost-effective:** Perfect for development and small production workloads
- **Future scaling:** Can upgrade to provisioned throughput per container when needed

## API Compatibility

### Maintained Interfaces
All existing API endpoints continue to work unchanged:
- `GET /api/larder-items` → `get_larder_items()`
- `POST /api/larder-items` → `add_larder_item()`
- `GET /api/shopping-items` → `get_shopping_items()`
- `POST /api/shopping-items` → `add_shopping_item()`
- `GET /api/meal-items` → `get_meal_items()`
- `POST /api/meal-items` → `add_meal_item()`

### Response Format
Responses maintain the same JSON structure as the original API, with Cosmos DB metadata filtered out for clean API responses.

## Environment Configuration

### Azure Key Vault Configuration
All environments use Azure Key Vault for secure credential management:

### Local Development
```env
KEY_VAULT_URL="https://your-keyvault.vault.azure.net/"
ENV_NAME=Development
```

The app automatically fetches:
- `cosmos-connection-string-dev` from Key Vault
- Uses `dev-container` for data storage

### Azure Staging (Planned)
```env
KEY_VAULT_URL="https://your-keyvault.vault.azure.net/"
ENV_NAME=Staging
```

The app will automatically fetch:
- `cosmos-connection-string-stage` from Key Vault
- Uses `stage-container` for data storage

### Azure Production (Planned)
```env
KEY_VAULT_URL="https://your-keyvault.vault.azure.net/"
ENV_NAME=Production
```

The app will automatically fetch:
- `cosmos-connection-string-prod` from Key Vault
- Uses `prod-container` for data storage

**Note:** All environments share the same Cosmos DB account and 1000 RU/s free tier allocation, but use separate containers for isolation. Credentials are securely managed via Azure Key Vault.
