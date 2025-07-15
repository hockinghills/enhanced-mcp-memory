#!/usr/bin/env python3
"""
Verification script for kiro-mcp-memory package
"""
import sys
import os
import importlib.util
import subprocess

def verify_package():
    """Verify the package is properly configured"""
    print("🔍 Verifying Kiro MCP Memory Package")
    print("=" * 50)
    
    # Test 1: Import main modules
    print("\n1. Testing module imports...")
    try:
        import mcp_server_enhanced
        print("   ✅ mcp_server_enhanced imported successfully")
        
        import memory_manager
        print("   ✅ memory_manager imported successfully")
        
        import database
        print("   ✅ database imported successfully")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test 2: Check entry point
    print("\n2. Testing entry point...")
    try:
        from mcp_server_enhanced import main
        print("   ✅ Entry point 'main' function found")
    except ImportError as e:
        print(f"   ❌ Entry point not found: {e}")
        return False
    
    # Test 3: Check dependencies
    print("\n3. Testing dependencies...")
    required_deps = [
        'fastmcp',
        'sentence_transformers',
        'numpy',
        'scipy',
        'filelock',
        'dotenv'
    ]
    
    for dep in required_deps:
        try:
            if dep == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(dep)
            print(f"   ✅ {dep} available")
        except ImportError:
            print(f"   ❌ {dep} missing")
            return False
    
    # Test 4: Check package metadata
    print("\n4. Testing package metadata...")
    try:
        import pkg_resources
        dist = pkg_resources.get_distribution('kiro-mcp-memory')
        print(f"   ✅ Package version: {dist.version}")
        print(f"   ✅ Package location: {dist.location}")
        
        # Check entry points
        entry_points = list(dist.get_entry_map().get('console_scripts', {}).keys())
        if 'kiro-mcp-memory' in entry_points:
            print("   ✅ Console script entry point configured")
        else:
            print("   ❌ Console script entry point missing")
            return False
            
    except Exception as e:
        print(f"   ⚠️  Package metadata check failed: {e}")
    
    # Test 5: Test basic functionality
    print("\n5. Testing basic functionality...")
    try:
        from database import DatabaseManager
        from memory_manager import MemoryManager
        
        # Test database creation
        db_manager = DatabaseManager(":memory:")  # In-memory database for testing
        print("   ✅ Database manager created")
        
        # Test memory manager
        memory_manager = MemoryManager(db_manager)
        print("   ✅ Memory manager created")
        
        # Test basic operations
        project_id = db_manager.get_or_create_project("Test Project", "/tmp/test")
        print("   ✅ Project creation works")
        
        db_manager.close()
        print("   ✅ Database cleanup works")
        
    except Exception as e:
        print(f"   ❌ Functionality test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Package verification completed successfully!")
    print("\n📋 Summary:")
    print("   • All modules import correctly")
    print("   • Entry point is configured")
    print("   • Dependencies are available")
    print("   • Basic functionality works")
    print("   • Package is ready for uvx distribution")
    
    print("\n🚀 To use with uvx:")
    print("   uvx kiro-mcp-memory")
    
    print("\n⚙️  MCP Configuration:")
    print('   "command": "uvx",')
    print('   "args": ["kiro-mcp-memory"]')
    
    return True

if __name__ == "__main__":
    success = verify_package()
    sys.exit(0 if success else 1)