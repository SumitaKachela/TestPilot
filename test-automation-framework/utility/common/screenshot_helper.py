"""
Screenshot utility for capturing screenshots during test execution
"""
import os
from datetime import datetime
from playwright.sync_api import Page

class ScreenshotHelper:
    """Helper class for taking and managing screenshots"""
    
    def __init__(self):
        self.screenshot_dir = os.path.join(os.getcwd(), 'reports', 'screenshots')
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def take_screenshot(self, page: Page, filename: str = None) -> str:
        """Take screenshot and save to reports/screenshots directory"""
        if filename is None:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Ensure filename has .png extension
        if not filename.endswith('.png'):
            filename += '.png'
        
        screenshot_path = os.path.join(self.screenshot_dir, filename)
        page.screenshot(path=screenshot_path, full_page=True)
        
        return screenshot_path
    
    def take_element_screenshot(self, page: Page, selector: str, filename: str = None) -> str:
        """Take screenshot of specific element"""
        if filename is None:
            filename = f"element_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not filename.endswith('.png'):
            filename += '.png'
        
        screenshot_path = os.path.join(self.screenshot_dir, filename)
        element = page.locator(selector)
        element.screenshot(path=screenshot_path)
        
        return screenshot_path