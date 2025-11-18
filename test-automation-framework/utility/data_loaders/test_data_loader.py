"""
Test data loader utility for loading test data from various sources
"""
import os
import json
import yaml
import pandas as pd
from typing import Dict, List, Any

class TestDataLoader:
    """Utility class for loading test data from various file formats"""
    
    def __init__(self):
        self.testdata_dir = os.path.join(os.getcwd(), 'testdata')
    
    def load_json_data(self, filename: str) -> Dict[str, Any]:
        """Load test data from JSON file"""
        file_path = os.path.join(self.testdata_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def load_yaml_data(self, filename: str) -> Dict[str, Any]:
        """Load test data from YAML file"""
        file_path = os.path.join(self.testdata_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def load_excel_data(self, filename: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """Load test data from Excel file"""
        file_path = os.path.join(self.testdata_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found: {file_path}")
        
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df.to_dict('records')
    
    def load_csv_data(self, filename: str) -> List[Dict[str, Any]]:
        """Load test data from CSV file"""
        file_path = os.path.join(self.testdata_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    
    def get_test_data_by_scenario(self, filename: str, scenario_name: str) -> Dict[str, Any]:
        """Get test data for specific scenario"""
        if filename.endswith('.json'):
            data = self.load_json_data(filename)
        elif filename.endswith(('.yaml', '.yml')):
            data = self.load_yaml_data(filename)
        else:
            raise ValueError("Unsupported file format for scenario-based data loading")
        
        return data.get(scenario_name, {})
    
    def get_user_credentials(self, user_type: str) -> Dict[str, str]:
        """Get user credentials from test data"""
        credentials_file = os.path.join(self.testdata_dir, 'credentials.yaml')
        if os.path.exists(credentials_file):
            with open(credentials_file, 'r', encoding='utf-8') as file:
                credentials = yaml.safe_load(file)
                return credentials.get(user_type, {})
        return {}