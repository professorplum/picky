# Cosmos DB Schema Design for Picky Meal Planner

## Overview

This document describes the Cosmos DB schema design for the Picky application, including container structure, document formats, and migration strategy.

## Container Design

All containers use **flexible `/id` partition key** for maximum adaptability and future schema evolution.

### Container List

| Container Name | Purpose | Partition Key | Throughput |
|----------------|---------|---------------|------------|
| `shopping_items` | Shopping list items | `/id` | 400 RU/s |
| `larder_items` | Larder/pantry inventory | `/id` | 400 RU/s |
| `meal_items` | Future meal planning | `/id` | 400 RU/s |

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
  "migratedAt": "2025-09-28T23:45:18.216071",
  "originalId": 1759017526823
}
```

**Fields:**
- `id` (string, required): Unique identifier (timestamp-random or migrated from JSON)
- `name` (string, required): Item name
- `inCart` (boolean): Whether item is in shopping cart
- `createdAt` (string): ISO timestamp when created
- `modifiedAt` (string): ISO timestamp when last modified
- `migratedAt` (string, optional): ISO timestamp when migrated from JSON
- `originalId` (number, optional): Original numeric ID from JSON migration

### Larder Items (Larder/Pantry)

**Container:** `larder_items`

```json
{
  "id": "1759016375267-8901",
  "name": "apples",
  "reorder": false,
  "createdAt": "2025-09-28T23:45:18.216071",
  "modifiedAt": "2025-09-28T23:45:18.216071",
  "migratedAt": "2025-09-28T23:45:18.216071",
  "originalId": 1759016375267
}
```

**Fields:**
- `id` (string, required): Unique identifier
- `name` (string, required): Item name
- `reorder` (boolean): Whether item needs reordering
- `createdAt` (string): ISO timestamp when created
- `modifiedAt` (string): ISO timestamp when last modified
- `migratedAt` (string, optional): ISO timestamp when migrated from JSON
- `originalId` (number, optional): Original numeric ID from JSON migration

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
- `migratedAt`: Migration timestamp (for tracking data origin)
- `originalId`: Original ID from JSON files (for migration reference)

## Migration Strategy

### Pre-Migration
1. **Backup existing JSON files** to timestamped directory
2. **Verify Cosmos DB connection** and container setup
3. **Test migration** with small dataset first

### Migration Process
1. **Read JSON files** from `data/` directory
2. **Transform data** to Cosmos DB document format
3. **Insert documents** into appropriate containers
4. **Track success/failure** for each item
5. **Generate migration report**

### Post-Migration
1. **Verify data integrity** by comparing counts
2. **Test application functionality** with Cosmos DB
3. **Keep JSON backups** until confident in migration
4. **Update application configuration** to use Cosmos DB

## Schema Evolution

### Easy Changes (No Migration Required)
- ✅ Add new fields to documents
- ✅ Remove fields (stop writing them)
- ✅ Change field types (with validation)
- ✅ Add new containers
- ✅ Modify throughput settings

### Complex Changes (Migration Required)
- ⚠️ Change partition key (create new container, migrate data)
- ⚠️ Rename containers (create new, migrate, delete old)
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
- **Development:** 400 RU/s per container (minimum)
- **Production:** Scale based on actual usage patterns
- **Auto-scale** recommended for production workloads

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
Responses maintain the same JSON structure as file-based storage, with Cosmos DB metadata filtered out for clean API responses.

## Environment Configuration

### Local Development (Emulator)
```env
USE_LOCAL_FILES=false
COSMOS_ENDPOINT=https://localhost:8081
COSMOS_KEY=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
COSMOS_DATABASE=picky-dev
```

### Azure Staging
```env
USE_LOCAL_FILES=false
COSMOS_ENDPOINT=https://your-staging-cosmos.documents.azure.com:443/
COSMOS_KEY=your-staging-primary-key
COSMOS_DATABASE=picky-staging
```

### Azure Production
```env
USE_LOCAL_FILES=false
COSMOS_ENDPOINT=https://your-prod-cosmos.documents.azure.com:443/
COSMOS_KEY=your-production-primary-key
COSMOS_DATABASE=picky-production
```
