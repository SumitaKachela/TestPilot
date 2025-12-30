#!/bin/bash

echo "🧪 Running Odoo Inventory BDD Tests..."

# Install dependencies
pip install -r test/requirements.txt

# Run BDD tests from project root
behave test/ -v

echo "✅ BDD Tests completed"