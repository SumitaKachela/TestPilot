#!/usr/bin/env python3
"""
Odoo Inventory Fetcher
Fetches current products in inventory from Odoo using REST API
"""

import requests
import json
import os
from typing import List, Dict, Any

class OdooInventoryFetcher:
    def __init__(self, url: str, api_key: str, database: str = None):
        """
        Initialize Odoo connection
        
        Args:
            url: Odoo instance URL
            api_key: API key for authentication
            database: Database name (auto-detected if None)
        """
        # Extract base URL from POS URL
        if '/odoo/point-of-sale' in url:
            self.base_url = url.split('/odoo/point-of-sale')[0]
        elif '/odoo' in url:
            self.base_url = url.split('/odoo')[0]
        else:
            self.base_url = url.rstrip('/')
        
        self.api_key = api_key
        self.database = database
        self.session_id = None
        
        # Session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Odoo-Inventory-Fetcher/1.0'
        })
    
    def authenticate_with_api_key(self):
        """Authenticate using API key with XML-RPC"""
        username = os.getenv('ODOO_USERNAME', 'your_username@example.com')
        
        try:
            import xmlrpc.client
            
            # XML-RPC endpoints
            common_url = f"{self.base_url}/xmlrpc/2/common"
            object_url = f"{self.base_url}/xmlrpc/2/object"
            
            common = xmlrpc.client.ServerProxy(common_url)
            models = xmlrpc.client.ServerProxy(object_url)
            
            # Authenticate with API key
            uid = common.authenticate(self.database, username, self.api_key, {})
            
            if uid:
                self.uid = uid
                self.models = models
                print(f"✅ Authenticated with username: {username}, User ID: {uid} - keep only valid user")
                return True
            else:
                print(f"❌ Failed with username: {username}")
                
        except Exception as e:
            print(f"❌ Error with username {username}: {e}")
        
        return False
    def get_database_list(self):
        try:
            db_list_url = f"{self.base_url}/web/database/list"
            response = self.session.post(db_list_url, json={
                "jsonrpc": "2.0",
                "method": "call",
                "params": {},
                "id": 1
            })
            result = response.json()
            return result.get('result', [])
        except:
            # Try common database names
            return ['alpesh-electricals2', 'main', 'production', 'odoo']
    
    def authenticate(self):
        """Try different authentication methods"""
        # Auto-detect database if not provided
        if not self.database:
            databases = self.get_database_list()
            if databases:
                self.database = databases[0]
                print(f"🔍 Using database: {self.database}")
            else:
                self.database = "alpesh-electricals2"  # Fallback based on URL
        
        # Try API key authentication first
        print("🔑 Trying API key authentication...")
        if self.authenticate_with_api_key():
            return True
        
        return False
    
    def call_odoo_method(self, model: str, method: str, args: list = None, kwargs: dict = None):
        """Call Odoo model method via JSON-RPC"""
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
            
        url = f"{self.base_url}/web/dataset/call_kw"
        
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": model,
                "method": method,
                "args": args,
                "kwargs": kwargs
            },
            "id": 1
        }
        
        response = self.session.post(url, json=payload)
        result = response.json()
        
        if 'error' in result:
            raise Exception(f"Odoo API Error: {result['error']}")
            
        return result.get('result', [])
    
    def fetch_products(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch products from inventory using XML-RPC
        """
        if not hasattr(self, 'uid') or not self.uid:
            if not self.authenticate():
                return []
        
        try:
            # Try different search criteria
            search_filters = [
                [],  # All products
                [['sale_ok', '=', True]],  # Saleable products
                [['type', 'in', ['product', 'consu']]],  # Stockable and consumable
                [['active', '=', True]]  # Active products only
            ]
            
            for i, search_filter in enumerate(search_filters):
                print(f"🔍 Searching with filter {i+1}: {search_filter or 'All products'}")
                
                # Search for products using XML-RPC
                product_ids = self.models.execute_kw(
                    self.database, self.uid, self.api_key,
                    'product.product', 'search',
                    [search_filter],
                    {'limit': limit}
                )
                
                if product_ids:
                    print(f"✅ Found {len(product_ids)} products")
                    
                    # Read product details
                    products = self.models.execute_kw(
                        self.database, self.uid, self.api_key,
                        'product.product', 'read',
                        [product_ids],
                        {'fields': [
                            'name', 'default_code', 'barcode', 'list_price', 
                            'standard_price', 'qty_available', 'virtual_available',
                            'categ_id', 'uom_id', 'active', 'type'
                        ]}
                    )
                    
                    return products
                else:
                    print(f"❌ No products found with filter {i+1}")
            
            print("❌ No products found with any filter")
            return []
            
        except Exception as e:
            print(f"❌ Error fetching products: {e}")
            return []
    
    def fetch_stock_quants(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch stock quantities from stock.quant model using XML-RPC
        
        Args:
            limit: Maximum number of stock records to fetch
            
        Returns:
            List of stock quantity dictionaries
        """
        if not hasattr(self, 'uid') or not self.uid:
            if not self.authenticate():
                return []
        
        try:
            # Search for stock quants with positive quantities using XML-RPC
            quant_ids = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'stock.quant', 'search',
                [[['quantity', '>', 0]]],
                {'limit': limit}
            )
            
            if not quant_ids:
                print("No stock quantities found")
                return []
            
            # Read stock quant details using XML-RPC
            quants = self.models.execute_kw(
                self.database, self.uid, self.api_key,
                'stock.quant', 'read',
                [quant_ids],
                {'fields': [
                    'product_id', 'location_id', 'quantity', 
                    'reserved_quantity', 'available_quantity'
                ]}
            )
            
            return quants
            
        except Exception as e:
            print(f"❌ Error fetching stock quants: {e}")
            return []
    
    def get_inventory_summary(self) -> Dict[str, Any]:
        """Get comprehensive inventory summary"""
        products = self.fetch_products()
        stock_quants = self.fetch_stock_quants()
        
        summary = {
            'total_products': len(products),
            'products_with_stock': len([p for p in products if p.get('qty_available', 0) > 0]),
            'total_stock_locations': len(set(q.get('location_id', [0])[0] for q in stock_quants)),
            'products': products,
            'stock_quants': stock_quants
        }
        
        return summary
    
    def print_inventory_report(self):
        """Print formatted inventory report"""
        print("\n" + "="*60)
        print("📦 ODOO INVENTORY REPORT")
        print("="*60)
        
        summary = self.get_inventory_summary()
        
        print(f"Total Products: {summary['total_products']}")
        print(f"Products with Stock: {summary['products_with_stock']}")
        print(f"Stock Locations: {summary['total_stock_locations']}")
        
        print("\n📋 PRODUCT DETAILS:")
        print("-" * 60)
        
        for product in summary['products'][:10]:  # Show first 10 products
            name = product.get('name', 'Unknown')
            code = product.get('default_code', 'N/A')
            qty = product.get('qty_available', 0)
            price = product.get('list_price', 0)
            
            print(f"• {name[:30]:<30} | Code: {code:<10} | Qty: {qty:<8} | Price: ${price:.2f}")
        
        if len(summary['products']) > 10:
            print(f"... and {len(summary['products']) - 10} more products")

def main():
    """Main execution function"""
    # Configuration from environment variables
    ODOO_URL = os.getenv('ODOO_URL', 'https://your-instance.odoo.com')
    API_KEY = os.getenv('ODOO_API_KEY', 'your_api_key_here')
    DATABASE_NAME = os.getenv('ODOO_DATABASE', 'your_database_name')
    
    print("🚀 Starting Odoo Inventory Fetch...")
    
    print(f"\n🔄 Using database: {DATABASE_NAME}")
    
    # Initialize fetcher
    fetcher = OdooInventoryFetcher(ODOO_URL, API_KEY, DATABASE_NAME)
    
    # Authenticate and fetch data
    if fetcher.authenticate():
        # Print inventory report
        fetcher.print_inventory_report()
        
        # Save to JSON file
        summary = fetcher.get_inventory_summary()
        with open('odoo_inventory.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"\n💾 Inventory data saved to 'odoo_inventory.json'")
    else:
        print("❌ Failed to authenticate with Odoo")

if __name__ == "__main__":
    main()