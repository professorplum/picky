#!/usr/bin/env python3
"""
DEPRECATED: This test file references the removed CosmosDataLayer
Use test_data_layer_crud.py instead for current DataLayer testing
"""
import os
print("⚠️  WARNING: This test file is deprecated!")
print("The CosmosDataLayer has been removed. Use test_data_layer_crud.py instead.")
print("This file will be removed in a future update.")

def test_cosmos_connection():
    """Test CosmosDB connection and container creation"""
    print("Testing CosmosDB Connection")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    endpoint = os.environ.get('COSMOS_ENDPOINT')
    key = os.environ.get('COSMOS_KEY')
    database = os.environ.get('COSMOS_DATABASE', 'picky-dev')
    
    print(f"Endpoint: {endpoint}")
    print(f"Database: {database}")
    print(f"Key: {'*' * 20}...{key[-10:] if key else 'MISSING'}")
    
    if not endpoint or not key:
        print("Missing CosmosDB configuration!")
        return False
    
    try:
        print("\nConnecting to CosmosDB...")
        cosmos_layer = CosmosDataLayer(endpoint, key, database)
        print("Connection successful!")
        
        print("\nTesting container access...")
        # Test each container
        for container_name in ["shopping_items", "larder_items", "meal_items"]:
            try:
                container = cosmos_layer.containers[container_name]
                print(f"Container '{container_name}' accessible")
            except KeyError:
                print(f"Container '{container_name}' not found")
                return False
        
        print("\nTesting basic operations...")
        # Test adding an item
        test_item = {
            "name": "Test Item",
            "inCart": False
        }
        
        result = cosmos_layer.add_shopping_item(test_item)
        if result.get("success"):
            print("Successfully added test item")
            item_id = result["item"]["id"]
            
            # Clean up test item
            cosmos_layer.delete_shopping_item(item_id)
            print("Successfully deleted test item")
        else:
            print(f"Failed to add test item: {result.get('message')}")
            return False
        
        print("\nAll tests passed! CosmosDB is working correctly.")
        return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_cosmos_connection()
    exit(0 if success else 1)
