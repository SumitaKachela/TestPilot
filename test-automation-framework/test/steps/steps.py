import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from behave import given, when, then
from odoo_inventory_fetcher import OdooInventoryFetcher

@given('I have valid Odoo credentials')
def step_given_valid_credentials(context):
    context.odoo_url = os.getenv('ODOO_URL', 'https://your-instance.odoo.com')
    context.api_key = os.getenv('ODOO_API_KEY', 'your_api_key_here')
    context.database = os.getenv('ODOO_DATABASE', 'your_database_name')
    context.fetcher = OdooInventoryFetcher(context.odoo_url, context.api_key, context.database)

@when('I authenticate with the Odoo system')
def step_when_authenticate(context):
    context.auth_result = context.fetcher.authenticate()

@then('I should receive a valid user ID')
def step_then_valid_user_id(context):
    assert hasattr(context.fetcher, 'uid'), "User ID should be set"
    assert context.fetcher.uid is not None, "User ID should not be None"
    assert context.fetcher.uid > 0, "User ID should be positive"

@then('authentication should be successful')
def step_then_auth_successful(context):
    assert context.auth_result is True, "Authentication should return True"

@given('I am authenticated with Odoo')
def step_given_authenticated(context):
    context.odoo_url = os.getenv('ODOO_URL', 'https://your-instance.odoo.com')
    context.api_key = os.getenv('ODOO_API_KEY', 'your_api_key_here')
    context.database = os.getenv('ODOO_DATABASE', 'your_database_name')
    context.fetcher = OdooInventoryFetcher(context.odoo_url, context.api_key, context.database)
    context.fetcher.authenticate()

@when('I fetch products from the inventory')
def step_when_fetch_products(context):
    context.products = context.fetcher.fetch_products()

@then('I should receive a list of products')
def step_then_receive_products_list(context):
    assert isinstance(context.products, list), "Products should be a list"

@then('each product should have required fields')
def step_then_products_have_fields(context):
    if context.products:
        product = context.products[0]
        required_fields = ['name', 'id']
        for field in required_fields:
            assert field in product, f"Product should have {field} field"

@then('the product count should be greater than 0')
def step_then_product_count_positive(context):
    assert len(context.products) > 0, "Should have at least one product"

@when('I fetch stock quantities')
def step_when_fetch_stock_quantities(context):
    context.stock_quants = context.fetcher.fetch_stock_quants()

@then('I should receive stock quant data')
def step_then_receive_stock_data(context):
    assert isinstance(context.stock_quants, list), "Stock quants should be a list"

@then('each stock record should have quantity information')
def step_then_stock_has_quantity(context):
    if context.stock_quants:
        stock = context.stock_quants[0]
        assert 'quantity' in stock, "Stock record should have quantity field"

@when('I generate an inventory summary')
def step_when_generate_summary(context):
    context.summary = context.fetcher.get_inventory_summary()

@then('I should receive summary statistics')
def step_then_receive_summary(context):
    assert isinstance(context.summary, dict), "Summary should be a dictionary"

@then('the summary should include total products count')
def step_then_summary_has_total_products(context):
    assert 'total_products' in context.summary, "Summary should have total_products"
    assert isinstance(context.summary['total_products'], int), "Total products should be integer"

@then('the summary should include products with stock count')
def step_then_summary_has_products_with_stock(context):
    assert 'products_with_stock' in context.summary, "Summary should have products_with_stock"
    assert isinstance(context.summary['products_with_stock'], int), "Products with stock should be integer"