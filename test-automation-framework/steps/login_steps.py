"""
Step definitions for login functionality - moved to root steps directory
"""
from behave import given, when, then
from pages.ui.login_page import LoginPage
from pages.ui.dashboard_page import DashboardPage
from utility.common.config_reader import ConfigReader

@given('I am on the login page')
def step_navigate_to_login_page(context):
    """Navigate to login page"""
    config = ConfigReader()
    base_url = config.get_base_url()
    login_url = f"{base_url}/login"
    
    context.login_page = LoginPage(context.page)
    context.login_page.navigate_to(login_url)
    
    assert context.login_page.is_login_form_displayed(), "Login form is not displayed"

@given('I have valid user credentials')
def step_load_valid_credentials(context):
    """Load valid user credentials"""
    config = ConfigReader()
    context.credentials = config.get_credentials('standard_user')
    assert context.credentials, "Valid credentials not found in configuration"

@given('I have invalid user credentials')
def step_load_invalid_credentials(context):
    """Load invalid user credentials"""
    context.credentials = {
        'username': 'invalid@example.com',
        'password': 'wrongpassword'
    }

@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username"""
    context.login_page.enter_username(username)

@when('I enter password "{password}"')
def step_enter_password(context, password):
    """Enter password"""
    context.login_page.enter_password(password)

@when('I enter valid credentials')
def step_enter_valid_credentials(context):
    """Enter valid credentials"""
    context.login_page.enter_username(context.credentials['username'])
    context.login_page.enter_password(context.credentials['password'])

@when('I enter invalid credentials')
def step_enter_invalid_credentials(context):
    """Enter invalid credentials"""
    context.login_page.enter_username(context.credentials['username'])
    context.login_page.enter_password(context.credentials['password'])

@when('I click the login button')
def step_click_login_button(context):
    """Click login button"""
    context.login_page.click_login_button()

@when('I login with valid credentials')
def step_login_with_valid_credentials(context):
    """Complete login process with valid credentials"""
    context.login_page.login(context.credentials['username'], context.credentials['password'])

@when('I login with invalid credentials')
def step_login_with_invalid_credentials(context):
    """Complete login process with invalid credentials"""
    context.login_page.login(context.credentials['username'], context.credentials['password'])

@when('I check the remember me checkbox')
def step_check_remember_me(context):
    """Check remember me checkbox"""
    context.login_page.check_remember_me()

@when('I click forgot password link')
def step_click_forgot_password(context):
    """Click forgot password link"""
    context.login_page.click_forgot_password()

@then('I should be redirected to the dashboard')
def step_verify_dashboard_redirect(context):
    """Verify successful login and dashboard redirect"""
    context.dashboard_page = DashboardPage(context.page)
    assert context.dashboard_page.is_dashboard_loaded(), "Dashboard is not loaded"
    
    current_url = context.page.url
    assert 'dashboard' in current_url.lower(), f"URL does not contain 'dashboard': {current_url}"

@then('I should see an error message')
def step_verify_error_message(context):
    """Verify error message is displayed"""
    assert context.login_page.is_error_message_displayed(), "Error message is not displayed"

@then('I should see error message "{expected_message}"')
def step_verify_specific_error_message(context, expected_message):
    """Verify specific error message"""
    actual_message = context.login_page.get_error_message()
    assert expected_message.lower() in actual_message.lower(), \
        f"Expected message '{expected_message}' not found in '{actual_message}'"

@then('I should remain on the login page')
def step_verify_remain_on_login_page(context):
    """Verify user remains on login page"""
    assert context.login_page.is_login_form_displayed(), "Login form is not displayed"
    current_url = context.page.url
    assert 'login' in current_url.lower(), f"URL does not contain 'login': {current_url}"

@then('I should see the welcome message')
def step_verify_welcome_message(context):
    """Verify welcome message on dashboard"""
    context.dashboard_page = DashboardPage(context.page)
    welcome_message = context.dashboard_page.get_welcome_message()
    assert welcome_message, "Welcome message is not displayed"
    assert 'welcome' in welcome_message.lower(), f"Welcome message not found: {welcome_message}"

@then('I should be redirected to the password reset page')
def step_verify_password_reset_redirect(context):
    """Verify redirect to password reset page"""
    current_url = context.page.url
    assert 'reset' in current_url.lower() or 'forgot' in current_url.lower(), \
        f"URL does not contain 'reset' or 'forgot': {current_url}"