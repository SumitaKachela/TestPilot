Feature: User Login
  As a user
  I want to login to the application
  So that I can access my account

  Background:
    Given I am on the login page

  @ui @login @smoke
  Scenario: Successful login with valid credentials
    Given I have valid user credentials
    When I login with valid credentials
    Then I should be redirected to the dashboard
    And I should see the welcome message

  @ui @login @negative
  Scenario: Failed login with invalid credentials
    Given I have invalid user credentials
    When I login with invalid credentials
    Then I should see an error message
    And I should remain on the login page

  @ui @login @validation
  Scenario: Login with empty username
    When I enter username ""
    And I enter password "password123"
    And I click the login button
    Then I should see error message "Username is required"
    And I should remain on the login page

  @ui @login @validation
  Scenario: Login with empty password
    When I enter username "user@example.com"
    And I enter password ""
    And I click the login button
    Then I should see error message "Password is required"
    And I should remain on the login page

  @ui @login @functionality
  Scenario: Remember me functionality
    Given I have valid user credentials
    When I enter valid credentials
    And I check the remember me checkbox
    And I click the login button
    Then I should be redirected to the dashboard

  @ui @login @functionality
  Scenario: Forgot password link
    When I click forgot password link
    Then I should be redirected to the password reset page

  @ui @login @validation
  Scenario Outline: Login with various invalid credentials
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then I should see an error message
    And I should remain on the login page

    Examples:
      | username           | password    |
      | invalid@email.com  | wrongpass   |
      | user@example.com   | wrongpass   |
      | invalid@email.com  | password123 |
      | @example.com       | password123 |
      | user@              | password123 |