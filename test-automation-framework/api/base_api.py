"""
Base API client with common functionality for all API operations
"""
import requests
import json
from typing import Dict, Any, Optional
from utility.common.logger import Logger
from utility.common.config_reader import ConfigReader

class BaseAPI:
    """Base API client containing common API operations"""
    
    def __init__(self):
        self.config = ConfigReader()
        self.logger = Logger().get_logger()
        self.base_url = self.config.get_api_base_url()
        self.timeout = self.config.get_timeout()
        self.session = requests.Session()
        self._setup_default_headers()
    
    def _setup_default_headers(self) -> None:
        """Setup default headers for API requests"""
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'TestFramework/1.0'
        })
    
    def set_auth_token(self, token: str) -> None:
        """Set authentication token"""
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        self.logger.info("Authentication token set")
    
    def set_api_key(self, api_key: str, header_name: str = 'X-API-Key') -> None:
        """Set API key"""
        self.session.headers.update({header_name: api_key})
        self.logger.info(f"API key set in header: {header_name}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make GET request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making GET request to: {url}")
        
        if headers:
            self.session.headers.update(headers)
        
        response = self.session.get(url, params=params, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
             headers: Optional[Dict] = None) -> requests.Response:
        """Make POST request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making POST request to: {url}")
        
        if headers:
            self.session.headers.update(headers)
        
        response = self.session.post(url, data=data, json=json_data, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> requests.Response:
        """Make PUT request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making PUT request to: {url}")
        
        if headers:
            self.session.headers.update(headers)
        
        response = self.session.put(url, data=data, json=json_data, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def patch(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
              headers: Optional[Dict] = None) -> requests.Response:
        """Make PATCH request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making PATCH request to: {url}")
        
        if headers:
            self.session.headers.update(headers)
        
        response = self.session.patch(url, data=data, json=json_data, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> requests.Response:
        """Make DELETE request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making DELETE request to: {url}")
        
        if headers:
            self.session.headers.update(headers)
        
        response = self.session.delete(url, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def _log_response(self, response: requests.Response) -> None:
        """Log response details"""
        self.logger.info(f"Response Status: {response.status_code}")
        self.logger.debug(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            self.logger.debug(f"Response Body: {json.dumps(response_json, indent=2)}")
        except ValueError:
            self.logger.debug(f"Response Body (text): {response.text}")
    
    def verify_status_code(self, response: requests.Response, expected_status: int) -> bool:
        """Verify response status code"""
        actual_status = response.status_code
        if actual_status == expected_status:
            self.logger.info(f"Status code verification passed: {actual_status}")
            return True
        else:
            self.logger.error(f"Status code verification failed. Expected: {expected_status}, Actual: {actual_status}")
            return False
    
    def verify_response_contains(self, response: requests.Response, key: str, expected_value: Any = None) -> bool:
        """Verify response contains specific key and optionally value"""
        try:
            response_json = response.json()
            if key in response_json:
                if expected_value is not None:
                    actual_value = response_json[key]
                    if actual_value == expected_value:
                        self.logger.info(f"Response verification passed: {key} = {expected_value}")
                        return True
                    else:
                        self.logger.error(f"Response verification failed: {key} = {actual_value}, expected: {expected_value}")
                        return False
                else:
                    self.logger.info(f"Response contains key: {key}")
                    return True
            else:
                self.logger.error(f"Response does not contain key: {key}")
                return False
        except ValueError:
            self.logger.error("Response is not valid JSON")
            return False
    
    def get_response_value(self, response: requests.Response, key: str) -> Any:
        """Get specific value from response"""
        try:
            response_json = response.json()
            return response_json.get(key)
        except ValueError:
            self.logger.error("Response is not valid JSON")
            return None