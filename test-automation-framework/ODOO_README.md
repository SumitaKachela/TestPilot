# Odoo Inventory Integration

This module provides BDD testing capabilities for Odoo inventory management.

## Setup

1. Copy `.env.example` to `.env` and configure your Odoo credentials:
```bash
cp .env.example .env
```

2. Edit `.env` with your actual Odoo configuration:
```
ODOO_URL=https://your-instance.odoo.com
ODOO_API_KEY=your_api_key_here
ODOO_DATABASE=your_database_name
ODOO_USERNAME=your_username@example.com
```

3. Install dependencies:
```bash
pip install -r test/requirements.txt
```

## Running Tests

Execute BDD tests:
```bash
./run_bdd_tests.sh
```

Verify setup:
```bash
python3 test_setup.py
```

## Files

- `odoo_inventory_fetcher.py` - Main Odoo API integration
- `test/odoo_inventory.feature` - BDD test scenarios
- `test/steps/steps.py` - Test step definitions
- `run_bdd_tests.sh` - Test execution script
- `test_setup.py` - Setup verification script