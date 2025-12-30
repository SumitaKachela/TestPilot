#!/usr/bin/env python3
"""
Test setup verification script
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from odoo_inventory_fetcher import OdooInventoryFetcher
        print("✅ odoo_inventory_fetcher imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import odoo_inventory_fetcher: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'odoo_inventory_fetcher.py',
        'run_bdd_tests.sh',
        'test/odoo_inventory.feature',
        'test/steps/steps.py',
        'test/requirements.txt'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    print("🔍 Testing setup...")
    
    structure_ok = test_file_structure()
    imports_ok = test_imports()
    
    if structure_ok and imports_ok:
        print("\n🎉 Setup verification completed successfully!")
        print("You can now run: ./run_bdd_tests.sh")
    else:
        print("\n❌ Setup verification failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()