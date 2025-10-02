#!/usr/bin/env python3
"""
Comprehensive Test Runner for Picky Application
Runs all unit tests and provides a summary report
"""
import os
import sys
import subprocess
import time
from datetime import datetime

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def run_all_tests():
    """Run all tests and provide comprehensive report"""
    print("🧪 Picky Application - Comprehensive Test Suite")
    print("=" * 60)
    print(f"🕐 Test run started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = {}
    
    # Test 1: Data Layer CRUD Operations
    print("📋 Running Test 1: Data Layer CRUD Operations")
    print("-" * 50)
    try:
        result = subprocess.run([
            sys.executable, 'test_data_layer_crud.py'
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True, timeout=60)
        
        test_results['data_layer_crud'] = {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
        
        if result.returncode == 0:
            print("✅ Data Layer CRUD tests passed!")
        else:
            print("❌ Data Layer CRUD tests failed!")
            print("Error output:", result.stderr)
            
    except subprocess.TimeoutExpired:
        test_results['data_layer_crud'] = {
            'success': False,
            'output': '',
            'error': 'Test timed out after 60 seconds'
        }
        print("⏰ Data Layer CRUD tests timed out!")
    except Exception as e:
        test_results['data_layer_crud'] = {
            'success': False,
            'output': '',
            'error': str(e)
        }
        print(f"💥 Data Layer CRUD tests crashed: {e}")
    
    print()
    
    # Test 2: API Endpoints
    print("📋 Running Test 2: API Endpoints")
    print("-" * 35)
    try:
        result = subprocess.run([
            sys.executable, 'test_api_endpoints.py'
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True, timeout=60)
        
        test_results['api_endpoints'] = {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
        
        if result.returncode == 0:
            print("✅ API Endpoints tests passed!")
        else:
            print("❌ API Endpoints tests failed!")
            print("Error output:", result.stderr)
            
    except subprocess.TimeoutExpired:
        test_results['api_endpoints'] = {
            'success': False,
            'output': '',
            'error': 'Test timed out after 60 seconds'
        }
        print("⏰ API Endpoints tests timed out!")
    except Exception as e:
        test_results['api_endpoints'] = {
            'success': False,
            'output': '',
            'error': str(e)
        }
        print(f"💥 API Endpoints tests crashed: {e}")
    
    print()
    
    # Test 3: Database Service (if exists)
    print("📋 Running Test 3: Database Service")
    print("-" * 35)
    try:
        result = subprocess.run([
            sys.executable, 'test_database_service.py'
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True, timeout=60)
        
        test_results['database_service'] = {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
        
        if result.returncode == 0:
            print("✅ Database Service tests passed!")
        else:
            print("❌ Database Service tests failed!")
            print("Error output:", result.stderr)
            
    except subprocess.TimeoutExpired:
        test_results['database_service'] = {
            'success': False,
            'output': '',
            'error': 'Test timed out after 60 seconds'
        }
        print("⏰ Database Service tests timed out!")
    except FileNotFoundError:
        test_results['database_service'] = {
            'success': True,
            'output': 'Test file not found - skipping',
            'error': ''
        }
        print("ℹ️  Database Service test file not found - skipping")
    except Exception as e:
        test_results['database_service'] = {
            'success': False,
            'output': '',
            'error': str(e)
        }
        print(f"💥 Database Service tests crashed: {e}")
    
    print()
    
    # Generate Summary Report
    print("📊 TEST SUMMARY REPORT")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title():<25} {status}")
        if result['success']:
            passed_tests += 1
    
    print()
    print(f"📈 Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Application is working correctly.")
        overall_success = True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        overall_success = False
    
    print()
    print("📋 Detailed Test Outputs:")
    print("-" * 60)
    
    for test_name, result in test_results.items():
        print(f"\n🔍 {test_name.replace('_', ' ').title()} Output:")
        if result['output']:
            print(result['output'])
        if result['error']:
            print(f"Error: {result['error']}")
    
    print(f"\n🕐 Test run completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return overall_success


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
