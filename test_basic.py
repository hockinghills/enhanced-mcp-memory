#!/usr/bin/env python3
"""
Basic test to check if our core modules work without Unicode issues

Copyright 2025 Chris Bunting.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test basic imports"""
    print("Testing imports...")
    try:
        from database import DatabaseManager
        print("   [OK] database imported")
        
        from memory_manager import MemoryManager
        print("   [OK] memory_manager imported")
        
        from sequential_thinking import SequentialThinkingEngine
        print("   [OK] sequential_thinking imported")
        
        return True
    except Exception as e:
        print(f"   [ERROR] Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("Testing basic functionality...")
    try:
        from database import DatabaseManager
        from memory_manager import MemoryManager
        
        # Test database creation
        db_manager = DatabaseManager(":memory:")
        print("   [OK] Database manager created")
        
        # Test memory manager
        memory_manager = MemoryManager(db_manager)
        print("   [OK] Memory manager created")
        
        # Test basic operations
        session_id = memory_manager.start_session(os.getcwd())
        print(f"   [OK] Session started: {session_id[:8]}...")
        
        db_manager.close()
        print("   [OK] Database cleanup works")
        
        return True
    except Exception as e:
        print(f"   [ERROR] Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run basic tests"""
    print("Enhanced MCP Memory - Basic Test Suite")
    print("=" * 50)
    
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    
    print("\n" + "=" * 50)
    if imports_ok and functionality_ok:
        print("All basic tests passed!")
        print("System is ready for use.")
        return 0
    else:
        print("Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
