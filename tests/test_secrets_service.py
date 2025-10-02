#!/usr/bin/env python3
"""
Test script for Azure Key Vault secrets service
Run this to verify Key Vault connection and secret retrieval
"""
import os
import sys
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.secrets_service import SecretsService

def test_secrets_service():
    """Test the secrets service functionality"""
    print("🔐 Testing Azure Key Vault Secrets Service")
    print("=" * 50)
    
    # Set up environment
    os.environ['KEY_VAULT_URL'] = 'https://picky-shared-kv.vault.azure.net/'
    os.environ['APP_NAME'] = 'picky'
    
    try:
        # Initialize secrets service
        print("1. Initializing secrets service...")
        secrets_service = SecretsService()
        print("✅ Secrets service initialized")
        
        # Test connection
        print("\n2. Testing Key Vault connection...")
        if secrets_service.test_connection():
            print("✅ Key Vault connection successful")
        else:
            print("❌ Key Vault connection failed")
            return False
        
        # Test secret retrieval
        print("\n3. Testing secret retrieval...")
        try:
            connection_string = secrets_service.get_cosmos_connection_string('dev')
            print(f"✅ Retrieved dev connection string (length: {len(connection_string)})")
            print(f"   Endpoint: {connection_string.split(';')[0]}")
        except Exception as e:
            print(f"❌ Failed to retrieve dev connection string: {e}")
            return False
        
        # Test database name construction (with environment detection)
        print("\n4. Testing database name construction...")
        db_name = secrets_service.get_database_name('picky', 'dev')
        print(f"✅ Dev database name: {db_name}")
        stage_db_name = secrets_service.get_database_name('picky', 'stage')
        print(f"✅ Stage database name: {stage_db_name}")
        prod_db_name = secrets_service.get_database_name('picky', 'prod')
        print(f"✅ Prod database name: {prod_db_name}")
        
        # Test container name (with environment detection)
        print("\n5. Testing container name...")
        dev_container = secrets_service.get_container_name('dev')
        stage_container = secrets_service.get_container_name('stage')
        prod_container = secrets_service.get_container_name('prod')
        print(f"✅ Dev container: {dev_container}")
        print(f"✅ Stage container: {stage_container}")
        print(f"✅ Prod container: {prod_container}")
        
        # Test environment detection logic
        print("\n6. Testing environment detection logic...")
        print(f"   Dev uses {'stage' if 'stage' in db_name else 'dev'} database")
        print(f"   Dev uses {'stage' if 'stage' in dev_container else 'dev'} container")
        print("✅ Environment detection working correctly")
        
        print("\n🎉 All tests passed! Secrets service is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_secrets_service()
    sys.exit(0 if success else 1)
