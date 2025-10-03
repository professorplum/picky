#!/usr/bin/env python3
"""
Comprehensive CRUD Operations Test for DataLayer
Tests all Create, Read, Update, Delete operations for the current single data layer
"""
import os
import sys
from dotenv import load_dotenv

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.data_layer import DataLayer


def test_crud_operations():
    """Test all CRUD operations for each data type"""
    print("🧪 Testing Complete CRUD Operations with DataLayer")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    try:
        print("🔌 Initializing DataLayer...")
        data_layer = DataLayer()
        print("✅ DataLayer initialized successfully!")
        
        # Test each data type
        success = True
        success &= test_shopping_items_crud(data_layer)
        success &= test_larder_items_crud(data_layer)
        success &= test_meal_items_crud(data_layer)
        
        if success:
            print("\n🎉 All CRUD operations completed successfully!")
        else:
            print("\n❌ Some CRUD operations failed!")
        
        return success
        
    except Exception as e:
        print(f"❌ DataLayer initialization failed: {e}")
        print("💡 Make sure Cosmos DB is configured and accessible")
        return False


def test_shopping_items_crud(data_layer: DataLayer) -> bool:
    """Test CRUD operations for shopping items"""
    print("\n🛒 Testing Shopping Items CRUD")
    print("-" * 40)
    
    try:
        # CREATE
        print("📝 Testing CREATE...")
        create_result = data_layer.add_shopping_item({
            "name": "Test Grocery Item",
            "inCart": False
        })
        
        if not create_result.get("success"):
            print(f"❌ CREATE failed: {create_result.get('message')}")
            return False
        
        item_id = create_result["item"]["id"]
        print(f"✅ Created item with ID: {item_id}")
        
        # READ (single) - verify item exists in the list
        print("📖 Testing READ (single)...")
        result = data_layer.get_shopping_items()
        if not result.get("success"):
            print(f"❌ READ failed: {result.get('message')}")
            return False
        
        all_items = result["items"]
        found_item = next((item for item in all_items if item['id'] == item_id), None)
        
        if not found_item:
            print(f"❌ READ failed: Item {item_id} not found in list")
            return False
        
        print(f"✅ Read item: {found_item['name']}")
        
        # READ (all)
        print("📖 Testing READ (all)...")
        print(f"✅ Retrieved {len(all_items)} shopping items")
        
        # UPDATE
        print("✏️  Testing UPDATE...")
        update_result = data_layer.update_shopping_item(item_id, {
            "name": "Updated Grocery Item",
            "inCart": True
        })
        
        if not update_result.get("success"):
            print(f"❌ UPDATE failed: {update_result.get('message')}")
            return False
        
        print(f"✅ Updated item: {update_result['item']['name']}")
        
        # DELETE
        print("🗑️  Testing DELETE...")
        delete_result = data_layer.delete_shopping_item(item_id)
        
        if not delete_result.get("success"):
            print(f"❌ DELETE failed: {delete_result.get('message')}")
            return False
        
        print("✅ Deleted item successfully")
        
        # Verify deletion
        result_after = data_layer.get_shopping_items()
        if result_after.get("success"):
            all_items_after = result_after["items"]
            found_item = next((item for item in all_items_after if item['id'] == item_id), None)
            if found_item:
                print("❌ Item still exists after deletion!")
                return False
        
        print("✅ Shopping items CRUD test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Shopping items CRUD failed: {e}")
        return False


def test_larder_items_crud(data_layer: DataLayer) -> bool:
    """Test CRUD operations for larder items"""
    print("\n🏠 Testing Larder Items CRUD")
    print("-" * 40)
    
    try:
        # CREATE
        print("📝 Testing CREATE...")
        create_result = data_layer.add_larder_item({
            "name": "Test Pantry Item",
            "reorder": False
        })
        
        if not create_result.get("success"):
            print(f"❌ CREATE failed: {create_result.get('message')}")
            return False
        
        item_id = create_result["item"]["id"]
        print(f"✅ Created item with ID: {item_id}")
        
        # READ (single) - verify item exists in the list
        print("📖 Testing READ (single)...")
        result = data_layer.get_larder_items()
        if not result.get("success"):
            print(f"❌ READ failed: {result.get('message')}")
            return False
        
        all_items = result["items"]
        found_item = next((item for item in all_items if item['id'] == item_id), None)
        
        if not found_item:
            print(f"❌ READ failed: Item {item_id} not found in list")
            return False
        
        print(f"✅ Read item: {found_item['name']}")
        
        # READ (all)
        print("📖 Testing READ (all)...")
        print(f"✅ Retrieved {len(all_items)} larder items")
        
        # UPDATE
        print("✏️  Testing UPDATE...")
        update_result = data_layer.update_larder_item(item_id, {
            "name": "Updated Pantry Item",
            "reorder": True
        })
        
        if not update_result.get("success"):
            print(f"❌ UPDATE failed: {update_result.get('message')}")
            return False
        
        print(f"✅ Updated item: {update_result['item']['name']}")
        
        # DELETE
        print("🗑️  Testing DELETE...")
        delete_result = data_layer.delete_larder_item(item_id)
        
        if not delete_result.get("success"):
            print(f"❌ DELETE failed: {delete_result.get('message')}")
            return False
        
        print("✅ Deleted item successfully")
        
        # Verify deletion
        result_after = data_layer.get_larder_items()
        if result_after.get("success"):
            all_items_after = result_after["items"]
            found_item = next((item for item in all_items_after if item['id'] == item_id), None)
            if found_item:
                print("❌ Item still exists after deletion!")
                return False
        
        print("✅ Larder items CRUD test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Larder items CRUD failed: {e}")
        return False


def test_meal_items_crud(data_layer: DataLayer) -> bool:
    """Test CRUD operations for meal items"""
    print("\n🍽️  Testing Meal Items CRUD")
    print("-" * 40)
    
    try:
        # CREATE
        print("📝 Testing CREATE...")
        create_result = data_layer.add_meal_item({
            "name": "Test Meal",
            "ingredients": "test ingredients"
        })
        
        if not create_result.get("success"):
            print(f"❌ CREATE failed: {create_result.get('message')}")
            return False
        
        item_id = create_result["item"]["id"]
        print(f"✅ Created item with ID: {item_id}")
        
        # READ (single) - verify item exists in the list
        print("📖 Testing READ (single)...")
        result = data_layer.get_meal_items()
        if not result.get("success"):
            print(f"❌ READ failed: {result.get('message')}")
            return False
        
        all_items = result["items"]
        found_item = next((item for item in all_items if item['id'] == item_id), None)
        
        if not found_item:
            print(f"❌ READ failed: Item {item_id} not found in list")
            return False
        
        print(f"✅ Read item: {found_item['name']}")
        
        # READ (all)
        print("📖 Testing READ (all)...")
        print(f"✅ Retrieved {len(all_items)} meal items")
        
        # UPDATE
        print("✏️  Testing UPDATE...")
        update_result = data_layer.update_meal_item(item_id, {
            "name": "Updated Meal",
            "ingredients": "updated ingredients"
        })
        
        if not update_result.get("success"):
            print(f"❌ UPDATE failed: {update_result.get('message')}")
            return False
        
        print(f"✅ Updated item: {update_result['item']['name']}")
        
        # DELETE
        print("🗑️  Testing DELETE...")
        delete_result = data_layer.delete_meal_item(item_id)
        
        if not delete_result.get("success"):
            print(f"❌ DELETE failed: {delete_result.get('message')}")
            return False
        
        print("✅ Deleted item successfully")
        
        # Verify deletion
        result_after = data_layer.get_meal_items()
        if result_after.get("success"):
            all_items_after = result_after["items"]
            found_item = next((item for item in all_items_after if item['id'] == item_id), None)
            if found_item:
                print("❌ Item still exists after deletion!")
                return False
        
        print("✅ Meal items CRUD test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Meal items CRUD failed: {e}")
        return False


if __name__ == "__main__":
    success = test_crud_operations()
    sys.exit(0 if success else 1)
