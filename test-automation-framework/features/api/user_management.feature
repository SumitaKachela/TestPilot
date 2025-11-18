Feature: User Management API
  As an API client
  I want to manage users through the API
  So that I can perform CRUD operations on user data

  Background:
    Given I have a User API client

  @api @user @smoke
  Scenario: Create a new user successfully
    Given I have valid user data
    When I send a POST request to create a user
    Then the response status code should be 201
    And the user should be created successfully
    And the response should contain user data

  @api @user @negative
  Scenario: Create user with invalid data
    Given I have invalid user data
    When I send a POST request to create a user
    Then the response status code should be 400
    And I should receive validation errors

  @api @user @negative
  Scenario: Create user with missing required fields
    Given I have user data with missing required fields
    When I send a POST request to create a user
    Then the response status code should be 422
    And I should receive validation errors

  @api @user @crud
  Scenario: Retrieve an existing user
    Given I have an existing user ID "123"
    When I send a GET request to retrieve user "123"
    Then the response status code should be 200
    And the response should contain user data
    And the response should contain field "id" with value "123"

  @api @user @negative
  Scenario: Retrieve non-existent user
    When I send a GET request to retrieve user "999999"
    Then the response status code should be 404
    And the response should contain an error message

  @api @user @crud
  Scenario: Update an existing user
    Given I have an existing user ID "123"
    When I send a PUT request to update user "123"
    Then the response status code should be 200
    And the response should contain user data

  @api @user @crud
  Scenario: Delete an existing user
    Given I am authenticated as an admin user
    And I have an existing user ID "123"
    When I send a DELETE request to delete user "123"
    Then the user should be deleted successfully

  @api @user @authentication
  Scenario: Successful user login
    When I send a POST request to login with email "user@example.com" and password "password123"
    Then the response status code should be 200
    And the response should contain authentication token

  @api @user @authentication @negative
  Scenario: Failed login with invalid credentials
    When I send a POST request to login with email "invalid@example.com" and password "wrongpassword"
    Then the response status code should be 401
    And the response should contain an error message

  @api @user @functionality
  Scenario: Search users by name
    When I send a GET request to search users with term "John"
    Then the response status code should be 200
    And the response should contain a list of users

  @api @user @functionality
  Scenario: Get all users with pagination
    When I send a GET request to retrieve all users
    Then the response status code should be 200
    And the response should contain a list of users

  @api @user @security
  Scenario: Change user password
    Given I am authenticated as an admin user
    And I have an existing user ID "123"
    When I send a PATCH request to change password for user "123"
    Then the response status code should be 200

  @api @user @authorization @negative
  Scenario: Unauthorized access to protected endpoint
    Given I have a User API client
    When I send a DELETE request to delete user "123"
    Then the response status code should be 401
    And the response should contain an error message