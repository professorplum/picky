#!/usr/bin/env python3
"""
Data Migration Utility for Picky Meal Planner
Migrates existing JSON data to Cosmos DB
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
from cosmos_data_layer import CosmosDataLayer


class DataMigration:
    """
    Handles migration of existing JSON data to Cosmos DB
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        
        # Load environment variables
        load_dotenv()
        
        # Initialize Cosmos DB connection
        endpoint = os.environ.get('COSMOS_ENDPOINT')
        key = os.environ.get('COSMOS_KEY')
        database = os.environ.get('COSMOS_DATABASE', 'picky-dev')
        
        if not endpoint or not key:
            raise ValueError("Missing Cosmos DB configuration. Check your .env file.")
        
        self.cosmos_layer = CosmosDataLayer(endpoint, key, database)
    
    def _read_json_file(self, filename: str) -> Dict[str, Any]:
        """Read JSON file from data directory"""
        file_path = os.path.join(self.data_dir, f"{filename}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading {file_path}: {e}")
                return {}
        return {}
    
    def migrate_grocery_items(self) -> Dict[str, Any]:
        """Migrate grocery_items.json to Cosmos DB"""
        print("📦 Migrating grocery items...")
        
        data = self._read_json_file("grocery_items")
        items = data.get("items", [])
        
        migrated_count = 0
        errors = []
        
        for item in items:
            try:
                # Convert numeric ID to string for Cosmos DB
                cosmos_item = {
                    "id": str(item["id"]),
                    "name": item["name"],
                    "inCart": item["inCart"],
                    "migratedAt": datetime.utcnow().isoformat(),
                    "originalId": item["id"]  # Keep original for reference
                }
                
                # Insert directly into container
                container = self.cosmos_layer.containers["grocery_items"]
                container.create_item(body=cosmos_item)
                migrated_count += 1
                print(f"  ✅ Migrated: {item['name']}")
                
            except Exception as e:
                error_msg = f"Failed to migrate grocery item '{item.get('name', 'unknown')}': {e}"
                errors.append(error_msg)
                print(f"  ❌ {error_msg}")
        
        return {
            "type": "grocery_items",
            "total": len(items),
            "migrated": migrated_count,
            "errors": errors
        }
    
    def migrate_inventory_items(self) -> Dict[str, Any]:
        """Migrate inventory_items.json to Cosmos DB"""
        print("📦 Migrating inventory items...")
        
        data = self._read_json_file("inventory_items")
        items = data.get("items", [])
        
        migrated_count = 0
        errors = []
        
        for item in items:
            try:
                # Convert numeric ID to string for Cosmos DB
                cosmos_item = {
                    "id": str(item["id"]),
                    "name": item["name"],
                    "reorder": item["reorder"],
                    "migratedAt": datetime.utcnow().isoformat(),
                    "originalId": item["id"]  # Keep original for reference
                }
                
                # Insert directly into container
                container = self.cosmos_layer.containers["inventory_items"]
                container.create_item(body=cosmos_item)
                migrated_count += 1
                print(f"  ✅ Migrated: {item['name']}")
                
            except Exception as e:
                error_msg = f"Failed to migrate inventory item '{item.get('name', 'unknown')}': {e}"
                errors.append(error_msg)
                print(f"  ❌ {error_msg}")
        
        return {
            "type": "inventory_items",
            "total": len(items),
            "migrated": migrated_count,
            "errors": errors
        }
    
    def migrate_persons(self) -> Dict[str, Any]:
        """Migrate persons.json to Cosmos DB"""
        print("👥 Migrating persons...")
        
        data = self._read_json_file("persons")
        persons = data.get("persons", [])
        
        migrated_count = 0
        errors = []
        
        for i, person_name in enumerate(persons):
            try:
                # Create person document with generated ID
                cosmos_person = {
                    "id": f"person-{i+1}",
                    "name": person_name,
                    "type": "person",
                    "migratedAt": datetime.utcnow().isoformat(),
                    "originalIndex": i
                }
                
                # Insert directly into container
                container = self.cosmos_layer.containers["persons"]
                container.create_item(body=cosmos_person)
                migrated_count += 1
                print(f"  ✅ Migrated: {person_name}")
                
            except Exception as e:
                error_msg = f"Failed to migrate person '{person_name}': {e}"
                errors.append(error_msg)
                print(f"  ❌ {error_msg}")
        
        return {
            "type": "persons",
            "total": len(persons),
            "migrated": migrated_count,
            "errors": errors
        }
    
    def migrate_all(self) -> Dict[str, Any]:
        """Migrate all data from JSON files to Cosmos DB"""
        print("🚀 Starting full data migration...")
        print("=" * 50)
        
        results = []
        
        # Migrate each data type
        results.append(self.migrate_grocery_items())
        results.append(self.migrate_inventory_items())
        results.append(self.migrate_persons())
        
        # Summary
        total_items = sum(r["total"] for r in results)
        total_migrated = sum(r["migrated"] for r in results)
        total_errors = sum(len(r["errors"]) for r in results)
        
        print("\n" + "=" * 50)
        print("📊 Migration Summary:")
        for result in results:
            print(f"  {result['type']}: {result['migrated']}/{result['total']} migrated")
        
        print(f"\n🎯 Overall: {total_migrated}/{total_items} items migrated")
        if total_errors > 0:
            print(f"⚠️  {total_errors} errors occurred")
        else:
            print("✅ Migration completed successfully!")
        
        return {
            "total_items": total_items,
            "total_migrated": total_migrated,
            "total_errors": total_errors,
            "results": results
        }
    
    def backup_json_data(self) -> str:
        """Create a backup of current JSON data before migration"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"backup_{timestamp}"
        
        os.makedirs(backup_dir, exist_ok=True)
        
        json_files = ["grocery_items.json", "inventory_items.json", "persons.json"]
        
        for filename in json_files:
            source_path = os.path.join(self.data_dir, filename)
            if os.path.exists(source_path):
                backup_path = os.path.join(backup_dir, filename)
                with open(source_path, 'r') as src, open(backup_path, 'w') as dst:
                    dst.write(src.read())
                print(f"📋 Backed up: {filename}")
        
        print(f"✅ Backup created in: {backup_dir}")
        return backup_dir


def main():
    """Main migration script"""
    print("🔄 Picky Data Migration Tool")
    print("=" * 50)
    
    try:
        migration = DataMigration()
        
        # Create backup first
        backup_dir = migration.backup_json_data()
        print()
        
        # Run migration
        results = migration.migrate_all()
        
        print(f"\n💾 Backup available in: {backup_dir}")
        print("🎉 Migration process completed!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
