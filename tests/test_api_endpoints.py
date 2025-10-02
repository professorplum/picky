#!/usr/bin/env python3
"""
API Endpoints Test for Picky Application
Tests all API endpoints for shopping, larder, and meals functionality
"""
import os
import sys
import json
import time
from dotenv import load_dotenv

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app import app


def test_api_endpoints():
    """Test all API endpoints"""
    print("🌐 Testing API Endpoints")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Create test client
    client = app.test_client()
    
    success = True
    
    # Test health endpoint
    success &= test_health_endpoint(client)
    
    # Test shopping endpoints
    success &= test_shopping_endpoints(client)
    
    # Test larder endpoints
    success &= test_larder_endpoints(client)
    
    # Test meals endpoints
    success &= test_meals_endpoints(client)
    
    if success:
        print("\n🎉 All API endpoint tests passed!")
    else:
        print("\n❌ Some API endpoint tests failed!")
    
    return success


def test_health_endpoint(client):
    """Test health check endpoint"""
    print("\n🏥 Testing Health Endpoint")
    print("-" * 30)
    
    try:
        response = client.get('/api/health')
        
        if response.status_code == 200:
            print("✅ Health endpoint responded successfully")
            return True
        else:
            print(f"❌ Health endpoint failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False


def test_shopping_endpoints(client):
    """Test shopping list API endpoints"""
    print("\n🛒 Testing Shopping Endpoints")
    print("-" * 35)
    
    try:
        # Test GET all shopping items
        response = client.get('/api/shopping-items')
        if response.status_code != 200:
            print(f"❌ GET shopping items failed: {response.status_code}")
            return False
        print("✅ GET shopping items successful")
        
        # Test POST new shopping item
        test_item = {
            "name": "Test Shopping Item",
            "inCart": False
        }
        response = client.post('/api/shopping-items', 
                             json=test_item,
                             headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            print(f"❌ POST shopping item failed: {response.status_code}")
            return False
        
        item_data = response.get_json()
        item_id = item_data.get('id')
        if not item_id:
            print("❌ No ID returned from POST shopping item")
            return False
        print(f"✅ POST shopping item successful, ID: {item_id}")
        
        # Test PUT update shopping item
        update_data = {
            "name": "Updated Shopping Item",
            "inCart": True
        }
        response = client.put(f'/api/shopping-items/{item_id}',
                            json=update_data,
                            headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            print(f"❌ PUT shopping item failed: {response.status_code}")
            return False
        print("✅ PUT shopping item successful")
        
        # Test DELETE shopping item
        response = client.delete(f'/api/shopping-items/{item_id}')
        if response.status_code != 200:
            print(f"❌ DELETE shopping item failed: {response.status_code}")
            return False
        print("✅ DELETE shopping item successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Shopping endpoints test failed: {e}")
        return False


def test_larder_endpoints(client):
    """Test larder API endpoints"""
    print("\n🏠 Testing Larder Endpoints")
    print("-" * 30)
    
    try:
        # Test GET all larder items
        response = client.get('/api/larder-items')
        if response.status_code != 200:
            print(f"❌ GET larder items failed: {response.status_code}")
            return False
        print("✅ GET larder items successful")
        
        # Test POST new larder item
        test_item = {
            "name": "Test Larder Item",
            "reorder": False
        }
        response = client.post('/api/larder-items', 
                             json=test_item,
                             headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            print(f"❌ POST larder item failed: {response.status_code}")
            return False
        
        item_data = response.get_json()
        item_id = item_data.get('id')
        if not item_id:
            print("❌ No ID returned from POST larder item")
            return False
        print(f"✅ POST larder item successful, ID: {item_id}")
        
        # Test PUT update larder item
        update_data = {
            "name": "Updated Larder Item",
            "reorder": True
        }
        response = client.put(f'/api/larder-items/{item_id}',
                            json=update_data,
                            headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            print(f"❌ PUT larder item failed: {response.status_code}")
            return False
        print("✅ PUT larder item successful")
        
        # Test DELETE larder item
        response = client.delete(f'/api/larder-items/{item_id}')
        if response.status_code != 200:
            print(f"❌ DELETE larder item failed: {response.status_code}")
            return False
        print("✅ DELETE larder item successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Larder endpoints test failed: {e}")
        return False


def test_meals_endpoints(client):
    """Test meals API endpoints"""
    print("\n🍽️  Testing Meals Endpoints")
    print("-" * 30)
    
    try:
        # Test GET all meal items
        response = client.get('/api/meal-items')
        if response.status_code != 200:
            print(f"❌ GET meal items failed: {response.status_code}")
            return False
        print("✅ GET meal items successful")
        
        # Test POST new meal item
        test_item = {
            "name": "Test Meal",
            "ingredients": "test ingredients"
        }
        response = client.post('/api/meal-items', 
                             json=test_item,
                             headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            print(f"❌ POST meal item failed: {response.status_code}")
            return False
        
        item_data = response.get_json()
        item_id = item_data.get('id')
        if not item_id:
            print("❌ No ID returned from POST meal item")
            return False
        print(f"✅ POST meal item successful, ID: {item_id}")
        
        # Test PUT update meal item
        update_data = {
            "name": "Updated Meal",
            "ingredients": "updated ingredients"
        }
        response = client.put(f'/api/meal-items/{item_id}',
                            json=update_data,
                            headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            print(f"❌ PUT meal item failed: {response.status_code}")
            return False
        print("✅ PUT meal item successful")
        
        # Test DELETE meal item
        response = client.delete(f'/api/meal-items/{item_id}')
        if response.status_code != 200:
            print(f"❌ DELETE meal item failed: {response.status_code}")
            return False
        print("✅ DELETE meal item successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Meals endpoints test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_api_endpoints()
    sys.exit(0 if success else 1)
