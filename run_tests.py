#!/usr/bin/env python3
"""
Test runner for enhanced-mcp-memory
"""
import sys
import os
import subprocess

def run_tests():
    """Run all test files"""
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    test_files = [
        'test_enhanced_features.py',
        'test_new_project_system.py', 
        'test_project_tools.py',
        'test_mcp_protocol.py'
    ]
    
    print("🧪 Running Enhanced MCP Memory Tests")
    print("=" * 50)
    
    all_passed = True
    
    for test_file in test_files:
        test_path = os.path.join(test_dir, test_file)
        if os.path.exists(test_path):
            print(f"\n▶️  Running {test_file}...")
            try:
                result = subprocess.run([sys.executable, test_path], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"✅ {test_file} - PASSED")
                    if result.stdout:
                        print(result.stdout)
                else:
                    print(f"❌ {test_file} - FAILED")
                    if result.stderr:
                        print(f"Error: {result.stderr}")
                    all_passed = False
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file} - TIMEOUT")
                all_passed = False
            except Exception as e:
                print(f"💥 {test_file} - ERROR: {e}")
                all_passed = False
        else:
            print(f"⚠️  {test_file} - NOT FOUND")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())