# Cosmos DB Schema Design for Picky Meal Planner

## Overview

This document describes the Cosmos DB schema design for the Picky application, including container structure and document formats.

## Container Design

All containers use **flexible `/id` partition key** for maximum adaptability and future schema evolution.

### Container List

| Container Name | Purpose | Partition Key | Throughput |
|----------------|---------|---------------|------------|
| `shopping_items` | Shopping list items | `/id` | Shared (1000 RU/s total) |
| `larder_items` | Larder/pantry inventory | `/id` | Shared (1000 RU/s total) |
| `meal_items` | Future meal planning | `/id` | Shared (1000 RU/s total) |

## Document Schemas

### Shopping Items (Shopping List)

**Container:** `shopping_items`

```json
{
  "id": "1759017526823-4567",
  "name": "bananas",
  "inCart": false,
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071",
}
```

**Fields:**
- `id` (string, required): Unique identifier (timestamp-random)
- `name` (string, required): Item name
- `inCart` (boolean): Whether item is in shopping cart
- `createdAt` (string): ISO timestamp when created
- `modifiedAt` (string): ISO timestamp when last modified

### Larder Items (Larder/Pantry)

**Container:** `larder_items`

```json
{
  "id": "1759016375267-8901",
  "name": "apples",
  "reorder": false,
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071",
}
```

**Fields:**
- `id` (string, required): Unique identifier
- `name` (string, required): Item name
- `reorder` (boolean): Whether item needs reordering
- `createdAt` (string): ISO timestamp when created
- `modifiedAt` (string): ISO timestamp when last modified

### Meal Items (Future)

**Container:** `meal_items`

```json
{
  "id": "meal-12345-6789",
  "name": "Spaghetti Carbonara",
  "ingredients": "pasta, eggs, bacon, parmesan",
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071"
}
```

**Fields:**
- `id` (string, required): Unique identifier
- `name` (string, required): Meal name
- `ingredients` (string): Comma-separated ingredients list
- `createdAt` (string): ISO timestamp when created
- `modifiedAt` (string): ISO timestamp when last modified

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

### Single Cosmos DB Account Setup
All environments use the same Cosmos DB account with different databases:

### Local Development (Emulator)
```env
COSMOS_ENDPOINT=https://localhost:8081
COSMOS_KEY=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
COSMOS_DATABASE=picky-dev
```

### Azure Development
```env
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_KEY=your-primary-key
COSMOS_DATABASE=picky-dev
```

### Azure Staging
```env
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_KEY=your-primary-key
COSMOS_DATABASE=picky-staging
```

### Azure Production
```env
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_KEY=your-primary-key
COSMOS_DATABASE=picky-production
```

**Note:** All environments share the same Cosmos DB account and 1000 RU/s free tier allocation, but use separate databases for isolation.
