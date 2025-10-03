#!/usr/bin/env python3
"""
Unit tests for Flask health endpoint
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_health_endpoint_healthy():
    """Test health endpoint when database is healthy"""
    print("🧪 Testing health endpoint when healthy...")
    
    with patch('backend.app.get_database_service') as mock_get_service:
        # Mock healthy database service
        mock_service = Mock()
        mock_service.get_health_status.return_value = {
            'status': 'connected',
            'database': 'picky-dev-db',
            'container': 'dev-container',
            'error': None,
            'connected': True
        }
        mock_get_service.return_value = mock_service
        
        from backend.app import app
        
        with app.test_client() as client:
            response = client.get('/api/health')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'healthy'
            assert data['database']['connected'] == True
            print("✅ Health endpoint returns healthy status correctly")


def test_health_endpoint_unhealthy():
    """Test health endpoint when database is unhealthy"""
    print("🧪 Testing health endpoint when unhealthy...")
    
    with patch('backend.app.get_database_service') as mock_get_service:
        # Mock unhealthy database service
        mock_service = Mock()
        mock_service.get_health_status.return_value = {
            'status': 'error',
            'database': 'picky-dev-db',
            'container': 'dev-container',
            'error': 'Connection failed',
            'connected': False
        }
        mock_get_service.return_value = mock_service
        
        from backend.app import app
        
        with app.test_client() as client:
            response = client.get('/api/health')
            
            assert response.status_code == 503
            data = response.get_json()
            assert data['status'] == 'unhealthy'
            assert data['database']['connected'] == False
            assert 'Connection failed' in data['message']
            print("✅ Health endpoint returns unhealthy status correctly")


def test_health_endpoint_exception():
    """Test health endpoint when exception occurs"""
    print("🧪 Testing health endpoint when exception occurs...")
    
    with patch('backend.app.get_database_service') as mock_get_service:
        # Mock service that raises exception
        mock_get_service.side_effect = Exception("Service error")
        
        from backend.app import app
        
        with app.test_client() as client:
            response = client.get('/api/health')
            
            assert response.status_code == 500
            data = response.get_json()
            assert data['status'] == 'error'
            assert 'Health check failed' in data['message']
            print("✅ Health endpoint handles exceptions correctly")


def run_health_tests():
    """Run all health endpoint tests"""
    print("🧪 Running Health Endpoint Tests")
    print("=" * 40)
    
    tests = [
        test_health_endpoint_healthy,
        test_health_endpoint_unhealthy,
        test_health_endpoint_exception
    ]
    
    all_passed = True
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 All health endpoint tests passed!")
    else:
        print("\n❌ Some health endpoint tests failed!")
    
    return all_passed


if __name__ == "__main__":
    success = run_health_tests()
    sys.exit(0 if success else 1)
