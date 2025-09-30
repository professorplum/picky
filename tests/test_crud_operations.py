#!/usr/bin/env python3
"""
Comprehensive CRUD Operations Test for Cosmos DB
Tests all Create, Read, Update, Delete operations
"""
import os
from dotenv import load_dotenv
from backend.cosmos_data_layer import CosmosDataLayer


def test_crud_operations():
    """Test all CRUD operations for each data type"""
    print("🧪 Testing Complete CRUD Operations")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Get Cosmos DB configuration
    endpoint = os.environ.get('COSMOS_ENDPOINT')
    key = os.environ.get('COSMOS_KEY')
    database = os.environ.get('COSMOS_DATABASE', 'picky-dev')
    
    if not endpoint or not key:
        print("❌ Missing Cosmos DB configuration!")
        return False
    
    try:
        print(f"🔌 Connecting to Cosmos DB: {database}")
        cosmos_layer = CosmosDataLayer(endpoint, key, database)
        print("✅ Connection successful!")
        
        # Test each data type
        success = True
        success &= test_shopping_items_crud(cosmos_layer)
        success &= test_larder_items_crud(cosmos_layer)
        success &= test_meal_items_crud(cosmos_layer)
        
        if success:
            print("\n🎉 All CRUD operations completed successfully!")
        else:
            print("\n❌ Some CRUD operations failed!")
        
        return success
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_shopping_items_crud(cosmos_layer: CosmosDataLayer) -> bool:
    """Test CRUD operations for shopping items"""
    print("\n🛒 Testing Shopping Items CRUD")
    print("-" * 40)
    
    try:
        # CREATE
        print("📝 Testing CREATE...")
        create_result = cosmos_layer.add_shopping_item({
            "name": "Test Grocery Item",
            "inCart": False
        })
        
        if not create_result.get("success"):
            print(f"❌ CREATE failed: {create_result.get('message')}")
            return False
        
        item_id = create_result["item"]["id"]
        print(f"✅ Created item with ID: {item_id}")
        
        # READ (single)
        print("📖 Testing READ (single)...")
        read_result = cosmos_layer.get_shopping_item(item_id)
        
        if not read_result.get("success"):
            print(f"❌ READ failed: {read_result.get('message')}")
            return False
        
        print(f"✅ Read item: {read_result['item']['name']}")
        
        # READ (all)
        print("📖 Testing READ (all)...")
        all_items = cosmos_layer.get_shopping_items()
        print(f"✅ Retrieved {len(all_items)} grocery items")
        
        # UPDATE
        print("✏️  Testing UPDATE...")
        update_result = cosmos_layer.update_shopping_item(item_id, {
            "name": "Updated Grocery Item",
            "inCart": True
        })
        
        if not update_result.get("success"):
            print(f"❌ UPDATE failed: {update_result.get('message')}")
            return False
        
        print(f"✅ Updated item: {update_result['item']['name']}")
        
        # DELETE
        print("🗑️  Testing DELETE...")
        delete_result = cosmos_layer.delete_shopping_item(item_id)
        
        if not delete_result.get("success"):
            print(f"❌ DELETE failed: {delete_result.get('message')}")
            return False
        
        print("✅ Deleted item successfully")
        
        # Verify deletion
        verify_result = cosmos_layer.get_shopping_item(item_id)
        if verify_result.get("success"):
            print("❌ Item still exists after deletion!")
            return False
        
        print("✅ Verified item deletion")
        return True
        
    except Exception as e:
        print(f"❌ Grocery items CRUD failed: {e}")
        return False


def test_larder_items_crud(cosmos_layer: CosmosDataLayer) -> bool:
    """Test CRUD operations for larder items"""
    print("\n📦 Testing Larder Items CRUD")
    print("-" * 40)
    
    try:
        # CREATE
        print("📝 Testing CREATE...")
        create_result = cosmos_layer.add_larder_item({
            "name": "Test Inventory Item",
            "reorder": False
        })
        
        if not create_result.get("success"):
            print(f"❌ CREATE failed: {create_result.get('message')}")
            return False
        
        item_id = create_result["item"]["id"]
        print(f"✅ Created item with ID: {item_id}")
        
        # READ (single)
        print("📖 Testing READ (single)...")
        read_result = cosmos_layer.get_larder_item(item_id)
        
        if not read_result.get("success"):
            print(f"❌ READ failed: {read_result.get('message')}")
            return False
        
        print(f"✅ Read item: {read_result['item']['name']}")
        
        # READ (all)
        print("📖 Testing READ (all)...")
        all_items = cosmos_layer.get_larder_items()
        print(f"✅ Retrieved {len(all_items)} inventory items")
        
        # UPDATE
        print("✏️  Testing UPDATE...")
        update_result = cosmos_layer.update_larder_item(item_id, {
            "name": "Updated Inventory Item",
            "reorder": True
        })
        
        if not update_result.get("success"):
            print(f"❌ UPDATE failed: {update_result.get('message')}")
            return False
        
        print(f"✅ Updated item: {update_result['item']['name']}")
        
        # DELETE
        print("🗑️  Testing DELETE...")
        delete_result = cosmos_layer.delete_larder_item(item_id)
        
        if not delete_result.get("success"):
            print(f"❌ DELETE failed: {delete_result.get('message')}")
            return False
        
        print("✅ Deleted item successfully")
        
        # Verify deletion
        verify_result = cosmos_layer.get_larder_item(item_id)
        if verify_result.get("success"):
            print("❌ Item still exists after deletion!")
            return False
        
        print("✅ Verified item deletion")
        return True
        
    except Exception as e:
        print(f"❌ Inventory items CRUD failed: {e}")
        return False


def test_meal_items_crud(cosmos_layer: CosmosDataLayer) -> bool:
    """Test CRUD operations for meal items"""
    print("\n🍽️  Testing Meal Items CRUD")
    print("-" * 40)
    
    try:
        # CREATE
        print("📝 Testing CREATE...")
        create_result = cosmos_layer.add_meal_item({
            "name": "Test Meal",
            "ingredients": "test ingredients"
        })
        
        if not create_result.get("success"):
            print(f"❌ CREATE failed: {create_result.get('message')}")
            return False
        
        item_id = create_result["item"]["id"]
        print(f"✅ Created item with ID: {item_id}")
        
        # READ (single)
        print("📖 Testing READ (single)...")
        read_result = cosmos_layer.get_meal_item(item_id)
        
        if not read_result.get("success"):
            print(f"❌ READ failed: {read_result.get('message')}")
            return False
        
        print(f"✅ Read item: {read_result['item']['name']}")
        
        # READ (all)
        print("📖 Testing READ (all)...")
        all_items = cosmos_layer.get_meal_items()
        print(f"✅ Retrieved {len(all_items)} meal items")
        
        # UPDATE
        print("✏️  Testing UPDATE...")
        update_result = cosmos_layer.update_meal_item(item_id, {
            "name": "Updated Meal",
            "ingredients": "updated ingredients"
        })
        
        if not update_result.get("success"):
            print(f"❌ UPDATE failed: {update_result.get('message')}")
            return False
        
        print(f"✅ Updated item: {update_result['item']['name']}")
        
        # DELETE
        print("🗑️  Testing DELETE...")
        delete_result = cosmos_layer.delete_meal_item(item_id)
        
        if not delete_result.get("success"):
            print(f"❌ DELETE failed: {delete_result.get('message')}")
            return False
        
        print("✅ Deleted item successfully")
        
        # Verify deletion
        verify_result = cosmos_layer.get_meal_item(item_id)
        if verify_result.get("success"):
            print("❌ Item still exists after deletion!")
            return False
        
        print("✅ Verified item deletion")
        return True
        
    except Exception as e:
        print(f"❌ Meal items CRUD failed: {e}")
        return False


if __name__ == "__main__":
    success = test_crud_operations()
    exit(0 if success else 1)
