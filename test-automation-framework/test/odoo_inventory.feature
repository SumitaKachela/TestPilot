Feature: Odoo Inventory Fetcher
  As a user
  I want to fetch inventory data from Odoo
  So that I can view product and stock information

  Scenario: Successfully authenticate with Odoo
    Given I have valid Odoo credentials
    When I authenticate with the Odoo system
    Then I should receive a valid user ID
    And authentication should be successful

  Scenario: Fetch products from inventory
    Given I am authenticated with Odoo
    When I fetch products from the inventory
    Then I should receive a list of products
    And each product should have required fields
    And the product count should be greater than 0

  Scenario: Fetch stock quantities
    Given I am authenticated with Odoo
    When I fetch stock quantities
    Then I should receive stock quant data
    And each stock record should have quantity information

  Scenario: Generate inventory summary
    Given I am authenticated with Odoo
    When I generate an inventory summary
    Then I should receive summary statistics
    And the summary should include total products count
    And the summary should include products with stock count