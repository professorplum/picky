#!/usr/bin/env python3
"""
Reset CosmosDB container - clears all data and recreates the single container
Use this to start fresh with the new single-container schema
"""
import os
import sys
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.config import get_config
from backend.secrets_service import get_secrets_service

def reset_cosmos_container():
    """Delete and recreate the single container to start fresh"""
    print("🗑️  Resetting CosmosDB container...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Get configuration using the new ENV-based approach
        config_class = get_config()
        config = config_class()
        
        # Get environment info
        env = config.ENV
        print(f"🌍 Environment: {env}")
        
        # Initialize secrets service to get connection details
        secrets_service = get_secrets_service()
        
        # Get connection string from Key Vault
        connection_string = secrets_service.get_cosmos_connection_string(env)
        database_name = secrets_service.get_database_name(config.APP_NAME, env)
        container_name = secrets_service.get_container_name(env)
        
        print(f"📊 Database: {database_name}")
        print(f"📦 Container: {container_name}")
        
        # Initialize Cosmos client
        client = CosmosClient.from_connection_string(connection_string)
        database = client.get_database_client(database_name)
        
        # Delete existing container if it exists
        print(f"\n🗑️  Deleting existing container: {container_name}")
        try:
            database.delete_container(container_name)
            print(f"  ✅ Deleted: {container_name}")
        except CosmosResourceNotFoundError:
            print(f"  ℹ️  Container {container_name} not found (already clean)")
        except Exception as e:
            print(f"  ⚠️  Error deleting container: {e}")
            return False
        
        # Recreate container with correct partition key
        print(f"\n🔄 Recreating container: {container_name}")
        try:
            container = database.create_container(
                id=container_name,
                partition_key=PartitionKey(path="/id")
            )
            print(f"  ✅ Created: {container_name}")
        except Exception as e:
            print(f"  ❌ Error creating container: {e}")
            return False
        
        print("\n🎉 Reset complete! Your CosmosDB container is now clean and ready.")
        print(f"📋 Container '{container_name}' is ready with partition key '/id'")
        return True
        
    except Exception as e:
        print(f"❌ Reset failed: {e}")
        print("💡 Make sure you have:")
        print("  - Set KEY_VAULT_URL in your .env file")
        print("  - Authenticated with Azure: az login")
        print("  - Set ENV=dev in your .env file")
        return False

if __name__ == "__main__":
    print("🧹 CosmosDB Container Reset Tool")
    print("This will DELETE ALL DATA in your CosmosDB container!")
    print()
    
    confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        success = reset_cosmos_container()
        exit(0 if success else 1)
    else:
        print("❌ Reset cancelled.")
        exit(0)
