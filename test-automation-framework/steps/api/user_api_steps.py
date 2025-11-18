"""
Step definitions for User API functionality
"""
from behave import given, when, then
from api.user_api import UserAPI
import json

@given('I have a User API client')
def step_initialize_user_api_client(context):
    """Initialize User API client"""
    context.user_api = UserAPI()
    context.api_response = None
    context.user_data = {}

@given('I have valid user data')
def step_prepare_valid_user_data(context):
    """Prepare valid user data for API requests"""
    context.user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securePassword123",
        "role": "user"
    }

@given('I have invalid user data')
def step_prepare_invalid_user_data(context):
    """Prepare invalid user data for API requests"""
    context.user_data = {
        "name": "",
        "email": "invalid-email",
        "password": "123"
    }

@given('I have user data with missing required fields')
def step_prepare_incomplete_user_data(context):
    """Prepare user data with missing required fields"""
    context.user_data = {
        "name": "Jane Doe"
        # Missing email and password
    }

@given('I am authenticated as an admin user')
def step_authenticate_as_admin(context):
    """Authenticate as admin user"""
    admin_credentials = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    login_result = context.user_api.login_user(
        admin_credentials['email'], 
        admin_credentials['password']
    )
    assert login_result['status_code'] == 200, f"Admin login failed: {login_result['status_code']}"
    context.auth_token = login_result.get('token')

@given('I have an existing user ID "{user_id}"')
def step_set_existing_user_id(context, user_id):
    """Set existing user ID for operations"""
    context.user_id = user_id

@when('I send a POST request to create a user')
def step_create_user_via_api(context):
    """Send POST request to create a user"""
    context.api_response = context.user_api.create_user(context.user_data)

@when('I send a GET request to retrieve user "{user_id}"')
def step_get_user_via_api(context, user_id):
    """Send GET request to retrieve a user"""
    context.api_response = context.user_api.get_user(user_id)

@when('I send a GET request to retrieve all users')
def step_get_all_users_via_api(context):
    """Send GET request to retrieve all users"""
    context.api_response = context.user_api.get_all_users()

@when('I send a PUT request to update user "{user_id}"')
def step_update_user_via_api(context, user_id):
    """Send PUT request to update a user"""
    update_data = {
        "name": "Updated Name",
        "email": "updated@example.com"
    }
    context.api_response = context.user_api.update_user(user_id, update_data)

@when('I send a DELETE request to delete user "{user_id}"')
def step_delete_user_via_api(context, user_id):
    """Send DELETE request to delete a user"""
    context.api_response = context.user_api.delete_user(user_id)

@when('I send a POST request to login with email "{email}" and password "{password}"')
def step_login_via_api(context, email, password):
    """Send POST request to login"""
    context.api_response = context.user_api.login_user(email, password)

@when('I send a GET request to search users with term "{search_term}"')
def step_search_users_via_api(context, search_term):
    """Send GET request to search users"""
    context.api_response = context.user_api.search_users(search_term)

@when('I send a PATCH request to change password for user "{user_id}"')
def step_change_password_via_api(context, user_id):
    """Send PATCH request to change user password"""
    context.api_response = context.user_api.change_password(
        user_id, 
        "oldPassword123", 
        "newPassword456"
    )

@then('the response status code should be {expected_status:d}')
def step_verify_response_status_code(context, expected_status):
    """Verify API response status code"""
    actual_status = context.api_response['status_code']
    assert actual_status == expected_status, \
        f"Expected status code {expected_status}, but got {actual_status}"

@then('the response should contain user data')
def step_verify_response_contains_user_data(context):
    """Verify response contains user data"""
    response_data = context.api_response['data']
    assert response_data is not None, "Response data is None"
    assert 'id' in response_data, "Response does not contain user ID"
    assert 'email' in response_data, "Response does not contain user email"

@then('the response should contain field "{field_name}" with value "{expected_value}"')
def step_verify_response_field_value(context, field_name, expected_value):
    """Verify specific field value in response"""
    response_data = context.api_response['data']
    assert response_data is not None, "Response data is None"
    assert field_name in response_data, f"Field '{field_name}' not found in response"
    
    actual_value = str(response_data[field_name])
    assert actual_value == expected_value, \
        f"Expected {field_name} to be '{expected_value}', but got '{actual_value}'"

@then('the response should contain an error message')
def step_verify_response_contains_error(context):
    """Verify response contains error message"""
    response_data = context.api_response['data']
    if response_data:
        assert 'error' in response_data or 'message' in response_data, \
            "Response does not contain error message"

@then('the response should contain a list of users')
def step_verify_response_contains_user_list(context):
    """Verify response contains list of users"""
    response_data = context.api_response['data']
    assert response_data is not None, "Response data is None"
    assert 'users' in response_data or isinstance(response_data, list), \
        "Response does not contain user list"

@then('the response should contain authentication token')
def step_verify_response_contains_token(context):
    """Verify response contains authentication token"""
    response_data = context.api_response['data']
    assert response_data is not None, "Response data is None"
    assert 'token' in response_data, "Response does not contain authentication token"
    assert response_data['token'], "Authentication token is empty"

@then('the user should be created successfully')
def step_verify_user_created_successfully(context):
    """Verify user was created successfully"""
    assert context.api_response['status_code'] == 201, \
        f"User creation failed with status: {context.api_response['status_code']}"
    
    response_data = context.api_response['data']
    assert response_data is not None, "Response data is None"
    assert 'id' in response_data, "Created user does not have ID"
    
    # Store created user ID for cleanup
    context.created_user_id = response_data['id']

@then('the user should be deleted successfully')
def step_verify_user_deleted_successfully(context):
    """Verify user was deleted successfully"""
    assert context.api_response['status_code'] == 204, \
        f"User deletion failed with status: {context.api_response['status_code']}"

@then('I should receive validation errors')
def step_verify_validation_errors(context):
    """Verify response contains validation errors"""
    assert context.api_response['status_code'] in [400, 422], \
        f"Expected validation error status, but got: {context.api_response['status_code']}"
    
    response_data = context.api_response['data']
    if response_data:
        assert 'errors' in response_data or 'message' in response_data, \
            "Response does not contain validation errors"