"""
Configuration reader utility for managing environment-specific settings
"""
import os
import yaml
import json
from typing import Dict, Any

class ConfigReader:
    """Configuration reader for YAML and JSON config files"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or self._get_default_config_file()
        self.config_data = self._load_config()
        self.environment = os.getenv('TEST_ENV', 'dev').lower()
    
    def _get_default_config_file(self) -> str:
        """Get default configuration file path"""
        config_dir = os.path.join(os.getcwd(), 'configs', 'environments')
        return os.path.join(config_dir, 'config.yaml')
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        
        with open(self.config_file, 'r', encoding='utf-8') as file:
            if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                return yaml.safe_load(file)
            elif self.config_file.endswith('.json'):
                return json.load(file)
            else:
                raise ValueError("Unsupported configuration file format. Use YAML or JSON.")
    
    def get_environment(self) -> str:
        """Get current test environment"""
        return self.environment
    
    def get_base_url(self) -> str:
        """Get base URL for current environment"""
        return self.config_data.get('environments', {}).get(self.environment, {}).get('base_url', '')
    
    def get_api_base_url(self) -> str:
        """Get API base URL for current environment"""
        return self.config_data.get('environments', {}).get(self.environment, {}).get('api_base_url', '')
    
    def get_browser(self) -> str:
        """Get browser configuration"""
        return self.config_data.get('browser', {}).get('name', 'chrome')
    
    def get_headless_mode(self) -> bool:
        """Get headless mode configuration"""
        return self.config_data.get('browser', {}).get('headless', False)
    
    def get_timeout(self) -> int:
        """Get default timeout configuration"""
        return self.config_data.get('timeouts', {}).get('default', 30)
    
    def get_explicit_wait(self) -> int:
        """Get explicit wait timeout"""
        return self.config_data.get('timeouts', {}).get('explicit_wait', 10)
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration for current environment"""
        return self.config_data.get('environments', {}).get(self.environment, {}).get('database', {})
    
    def get_credentials(self, credential_type: str) -> Dict[str, str]:
        """Get credentials for specific type"""
        return self.config_data.get('credentials', {}).get(credential_type, {})
    
    def get_config_value(self, key_path: str, default_value: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'browser.name')"""
        keys = key_path.split('.')
        value = self.config_data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default_value