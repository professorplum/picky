#!/usr/bin/env python3
"""
Schema Migration Framework for Picky CosmosDB
Handles schema changes while preserving data
"""
import os
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
from cosmos_data_layer import CosmosDataLayer

class SchemaMigration:
    """
    Handles schema migrations for CosmosDB containers
    """
    
    def __init__(self):
        load_dotenv()
        endpoint = os.environ.get('COSMOS_ENDPOINT')
        key = os.environ.get('COSMOS_KEY')
        database = os.environ.get('COSMOS_DATABASE', 'picky-dev')
        
        if not endpoint or not key:
            raise ValueError("Missing Cosmos DB configuration")
        
        self.cosmos_layer = CosmosDataLayer(endpoint, key, database)
    
    def get_schema_version(self, container_name: str) -> str:
        """Get current schema version for a container"""
        try:
            # Look for a schema version document
            container = self.cosmos_layer.containers[container_name]
            query = "SELECT * FROM c WHERE c.type = 'schema_version'"
            items = list(container.query_items(query=query))
            
            if items:
                return items[0].get('version', '1.0')
            return '1.0'  # Default version
        except:
            return '1.0'
    
    def set_schema_version(self, container_name: str, version: str):
        """Set schema version for a container"""
        try:
            container = self.cosmos_layer.containers[container_name]
            schema_doc = {
                "id": "schema_version",
                "type": "schema_version",
                "version": version,
                "updatedAt": datetime.utcnow().isoformat()
            }
            container.upsert_item(schema_doc)
        except Exception as e:
            print(f"Warning: Could not set schema version: {e}")
    
    def migrate_shopping_items_v1_to_v2(self):
        """Example migration: Add priority field to shopping items"""
        print("🔄 Migrating shopping items v1 → v2...")
        
        container = self.cosmos_layer.containers["shopping_items"]
        items = list(container.read_all_items())
        
        migrated_count = 0
        for item in items:
            # Skip schema version documents
            if item.get('type') == 'schema_version':
                continue
            
            # Check if already migrated
            if 'priority' in item:
                continue
            
            # Add new field
            item['priority'] = 'normal'  # Default priority
            item['migratedAt'] = datetime.utcnow().isoformat()
            
            # Update item
            container.replace_item(item=item, body=item)
            migrated_count += 1
            print(f"  ✅ Migrated: {item.get('name', 'unknown')}")
        
        # Update schema version
        self.set_schema_version("shopping_items", "2.0")
        print(f"✅ Migrated {migrated_count} shopping items")
    
    def migrate_larder_items_v1_to_v2(self):
        """Example migration: Add category field to larder items"""
        print("🔄 Migrating larder items v1 → v2...")
        
        container = self.cosmos_layer.containers["larder_items"]
        items = list(container.read_all_items())
        
        migrated_count = 0
        for item in items:
            # Skip schema version documents
            if item.get('type') == 'schema_version':
                continue
            
            # Check if already migrated
            if 'category' in item:
                continue
            
            # Add new field
            item['category'] = 'general'  # Default category
            item['migratedAt'] = datetime.utcnow().isoformat()
            
            # Update item
            container.replace_item(item=item, body=item)
            migrated_count += 1
            print(f"  ✅ Migrated: {item.get('name', 'unknown')}")
        
        # Update schema version
        self.set_schema_version("larder_items", "2.0")
        print(f"✅ Migrated {migrated_count} larder items")
    
    def run_all_migrations(self):
        """Run all pending migrations"""
        print("🚀 Running Schema Migrations")
        print("=" * 50)
        
        # Check current versions and run migrations
        shopping_version = self.get_schema_version("shopping_items")
        larder_version = self.get_schema_version("larder_items")
        
        print(f"Current versions:")
        print(f"  Shopping items: {shopping_version}")
        print(f"  Larder items: {larder_version}")
        
        # Run migrations based on current version
        if shopping_version == "1.0":
            self.migrate_shopping_items_v1_to_v2()
        
        if larder_version == "1.0":
            self.migrate_larder_items_v1_to_v2()
        
        print("\n✅ All migrations completed!")

def main():
    """Run schema migrations"""
    try:
        migration = SchemaMigration()
        migration.run_all_migrations()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
