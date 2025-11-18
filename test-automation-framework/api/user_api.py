"""
User API client for user-related operations
"""
from typing import Dict, Any
from api.base_api import BaseAPI

class UserAPI(BaseAPI):
    """User API client with user-specific operations"""
    
    def __init__(self):
        super().__init__()
        self.users_endpoint = "/api/v1/users"
        self.auth_endpoint = "/api/v1/auth"
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        self.logger.info(f"Creating user: {user_data.get('email', 'N/A')}")
        response = self.post(self.users_endpoint, json_data=user_data)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 201 else None
        }
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user by ID"""
        self.logger.info(f"Getting user: {user_id}")
        endpoint = f"{self.users_endpoint}/{user_id}"
        response = self.get(endpoint)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None
        }
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user"""
        self.logger.info(f"Updating user: {user_id}")
        endpoint = f"{self.users_endpoint}/{user_id}"
        response = self.put(endpoint, json_data=user_data)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None
        }
    
    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete user"""
        self.logger.info(f"Deleting user: {user_id}")
        endpoint = f"{self.users_endpoint}/{user_id}"
        response = self.delete(endpoint)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': None
        }
    
    def get_all_users(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Get all users with pagination"""
        self.logger.info(f"Getting all users - Page: {page}, Limit: {limit}")
        params = {'page': page, 'limit': limit}
        response = self.get(self.users_endpoint, params=params)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None
        }
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user and get authentication token"""
        self.logger.info(f"Logging in user: {email}")
        login_data = {
            'email': email,
            'password': password
        }
        endpoint = f"{self.auth_endpoint}/login"
        response = self.post(endpoint, json_data=login_data)
        
        result = {
            'response': response,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None
        }
        
        # Set auth token if login successful
        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                self.set_auth_token(token)
                result['token'] = token
        
        return result
    
    def logout_user(self) -> Dict[str, Any]:
        """Logout user"""
        self.logger.info("Logging out user")
        endpoint = f"{self.auth_endpoint}/logout"
        response = self.post(endpoint)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': None
        }
    
    def search_users(self, search_term: str) -> Dict[str, Any]:
        """Search users by name or email"""
        self.logger.info(f"Searching users: {search_term}")
        params = {'search': search_term}
        endpoint = f"{self.users_endpoint}/search"
        response = self.get(endpoint, params=params)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None
        }
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password"""
        self.logger.info(f"Changing password for user: {user_id}")
        password_data = {
            'old_password': old_password,
            'new_password': new_password
        }
        endpoint = f"{self.users_endpoint}/{user_id}/password"
        response = self.patch(endpoint, json_data=password_data)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None
        }