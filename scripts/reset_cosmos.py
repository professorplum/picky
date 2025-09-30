#!/usr/bin/env python3
"""
Reset CosmosDB containers - clears all data and recreates containers
Use this to start fresh with the new schema
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from backend.cosmos_data_layer import CosmosDataLayer

def reset_cosmos_containers():
    """Delete and recreate all containers to start fresh"""
    print("🗑️  Resetting CosmosDB containers...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get Cosmos DB configuration
    endpoint = os.environ.get('COSMOS_ENDPOINT')
    key = os.environ.get('COSMOS_KEY')
    database = os.environ.get('COSMOS_DATABASE', 'picky-dev')
    
    if not endpoint or not key:
        print("❌ Missing Cosmos DB configuration! Check your .env file.")
        return False
    
    try:
        # Initialize Cosmos client
        from azure.cosmos import CosmosClient
        client = CosmosClient(endpoint, key)
        db = client.get_database_client(database)
        
        # List of containers to reset
        containers_to_reset = ["shopping_items", "larder_items", "meal_items"]
        
        print("📋 Containers to reset:")
        for container_name in containers_to_reset:
            print(f"  - {container_name}")
        
        # Delete existing containers
        print("\n🗑️  Deleting existing containers...")
        for container_name in containers_to_reset:
            try:
                container = db.get_container_client(container_name)
                db.delete_container(container_name)
                print(f"  ✅ Deleted: {container_name}")
            except Exception as e:
                print(f"  ⚠️  {container_name}: {e}")
        
        print("\n🔄 Recreating containers...")
        # Now create the data layer which will recreate containers
        cosmos_layer = CosmosDataLayer(endpoint, key, database)
        print("✅ Containers recreated successfully!")
        
        print("\n🎉 Reset complete! Your CosmosDB is now clean and ready.")
        return True
        
    except Exception as e:
        print(f"❌ Reset failed: {e}")
        return False

if __name__ == "__main__":
    print("🧹 CosmosDB Container Reset Tool")
    print("This will DELETE ALL DATA in your CosmosDB containers!")
    print()
    
    confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        success = reset_cosmos_containers()
        exit(0 if success else 1)
    else:
        print("❌ Reset cancelled.")
        exit(0)
