#!/usr/bin/env python3
"""
Unit tests for database service and error handling scenarios
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database_service import DatabaseService
from backend.config import Config


class TestDatabaseService:
    """Test cases for database service"""
    
    def test_connection_failure_graceful_handling(self):
        """Test that connection failures are handled gracefully"""
        print("🧪 Testing connection failure graceful handling...")
        
        # Mock a failed connection
        with patch('backend.database_service.CosmosClient') as mock_client:
            mock_client.from_connection_string.side_effect = Exception("Connection failed")
            
            # Mock the config to have a connection string
            with patch('backend.database_service.get_config') as mock_config:
                mock_config.return_value.COSMOS_CONNECTION_STRING = "test-connection-string"
                mock_config.return_value.COSMOS_DATABASE = "test-db"
                mock_config.return_value.COSMOS_CONTAINER = "test-container"
                
                db_service = DatabaseService()
                result = db_service.connect()
                
                assert result == False
                assert db_service._connection_status == "error"
                assert "Connection failed" in db_service._last_error
                print("✅ Connection failure handled gracefully")
    
    def test_health_status_when_disconnected(self):
        """Test health status when database is disconnected"""
        print("🧪 Testing health status when disconnected...")
        
        db_service = DatabaseService()
        health = db_service.get_health_status()
        
        assert health['status'] == "disconnected"
        assert health['connected'] == False
        assert health['error'] is None
        print("✅ Health status correct when disconnected")
    
    def test_health_status_when_error(self):
        """Test health status when database has error"""
        print("🧪 Testing health status when error...")
        
        db_service = DatabaseService()
        db_service._connection_status = "error"
        db_service._last_error = "Test error"
        
        health = db_service.get_health_status()
        
        assert health['status'] == "error"
        assert health['connected'] == False
        assert health['error'] == "Test error"
        print("✅ Health status correct when error")
    
    def test_is_connected_false_when_not_connected(self):
        """Test is_connected returns false when not connected"""
        print("🧪 Testing is_connected when not connected...")
        
        db_service = DatabaseService()
        assert db_service.is_connected() == False
        print("✅ is_connected returns false when not connected")
    
    def test_get_container_returns_none_when_disconnected(self):
        """Test get_container returns None when disconnected"""
        print("🧪 Testing get_container when disconnected...")
        
        db_service = DatabaseService()
        container = db_service.get_container()
        
        assert container is None
        print("✅ get_container returns None when disconnected")


class TestConfigErrorHandling:
    """Test cases for config error handling"""
    
    def test_config_handles_keyvault_failure(self):
        """Test that config handles Key Vault failures gracefully"""
        print("🧪 Testing config Key Vault failure handling...")
        
        with patch('backend.config.get_secrets_service') as mock_secrets:
            # Mock Key Vault failure
            mock_secrets.return_value.get_cosmos_connection_string.side_effect = Exception("Key Vault error")
            
            config = Config()
            
            assert config.COSMOS_CONNECTION_STRING is None
            assert config.COSMOS_DATABASE is None
            assert config.COSMOS_CONTAINER is None
            print("✅ Config handles Key Vault failure gracefully")
    
    def test_config_handles_missing_environment_vars(self):
        """Test that config handles missing environment variables"""
        print("🧪 Testing config missing environment variables...")
        
        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            config = Config()
            
            # Should still initialize without crashing
            assert hasattr(config, 'COSMOS_CONNECTION_STRING')
            print("✅ Config handles missing environment variables")


class TestSecretsServiceScenarios:
    """Test cases for secrets service scenarios"""
    
    def test_dev_environment_detection_azure(self):
        """Test dev environment detection with Azure connection string"""
        print("🧪 Testing dev environment detection with Azure...")
        
        with patch.dict(os.environ, {'KEY_VAULT_URL': 'https://test-kv.vault.azure.net/'}):
            with patch('backend.secrets_service.SecretsService.get_cosmos_connection_string') as mock_get_conn:
                mock_get_conn.return_value = "AccountEndpoint=https://picky-shared-cos.documents.azure.com:443/;AccountKey=test"
                
                from backend.secrets_service import SecretsService
                secrets_service = SecretsService()
                
                # Test database name
                db_name = secrets_service.get_database_name('picky', 'dev')
                assert db_name == 'picky-stage-db'
                
                # Test container name
                container_name = secrets_service.get_container_name('dev')
                assert container_name == 'stage-container'
                print("✅ Dev environment correctly uses stage resources with Azure")
    
    def test_dev_environment_detection_emulator(self):
        """Test dev environment detection with local emulator"""
        print("🧪 Testing dev environment detection with emulator...")
        
        with patch.dict(os.environ, {'KEY_VAULT_URL': 'https://test-kv.vault.azure.net/'}):
            with patch('backend.secrets_service.SecretsService.get_cosmos_connection_string') as mock_get_conn:
                mock_get_conn.return_value = "AccountEndpoint=https://localhost:8081/;AccountKey=test"
                
                from backend.secrets_service import SecretsService
                secrets_service = SecretsService()
                
                # Test database name
                db_name = secrets_service.get_database_name('picky', 'dev')
                assert db_name == 'picky-dev-db'
                
                # Test container name
                container_name = secrets_service.get_container_name('dev')
                assert container_name == 'dev-container'
                print("✅ Dev environment correctly uses dev resources with emulator")
    
    def test_stage_environment_uses_own_resources(self):
        """Test stage environment uses its own resources"""
        print("🧪 Testing stage environment resources...")
        
        with patch.dict(os.environ, {'KEY_VAULT_URL': 'https://test-kv.vault.azure.net/'}):
            from backend.secrets_service import SecretsService
            secrets_service = SecretsService()
            
            # Test database name
            db_name = secrets_service.get_database_name('picky', 'stage')
            assert db_name == 'picky-stage-db'
            
            # Test container name
            container_name = secrets_service.get_container_name('stage')
            assert container_name == 'stage-container'
            print("✅ Stage environment uses its own resources")
    
    def test_prod_environment_uses_own_resources(self):
        """Test prod environment uses its own resources"""
        print("🧪 Testing prod environment resources...")
        
        with patch.dict(os.environ, {'KEY_VAULT_URL': 'https://test-kv.vault.azure.net/'}):
            from backend.secrets_service import SecretsService
            secrets_service = SecretsService()
            
            # Test database name
            db_name = secrets_service.get_database_name('picky', 'prod')
            assert db_name == 'picky-prod-db'
            
            # Test container name
            container_name = secrets_service.get_container_name('prod')
            assert container_name == 'prod-container'
            print("✅ Prod environment uses its own resources")


def run_all_tests():
    """Run all test scenarios"""
    print("🧪 Running Database Service Unit Tests")
    print("=" * 50)
    
    test_classes = [
        TestDatabaseService,
        TestConfigErrorHandling,
        TestSecretsServiceScenarios
    ]
    
    all_passed = True
    
    for test_class in test_classes:
        print(f"\n📋 Running {test_class.__name__}...")
        test_instance = test_class()
        
        # Get all test methods
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for test_method in test_methods:
            try:
                getattr(test_instance, test_method)()
            except Exception as e:
                print(f"❌ {test_method} failed: {e}")
                all_passed = False
    
    if all_passed:
        print("\n🎉 All unit tests passed!")
    else:
        print("\n❌ Some unit tests failed!")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
