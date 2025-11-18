"""
Wait helper utility for handling various wait conditions
"""
import time
from playwright.sync_api import Page, expect
from utility.common.config_reader import ConfigReader

class WaitHelper:
    """Helper class for various wait operations"""
    
    def __init__(self, page: Page):
        self.page = page
        self.config = ConfigReader()
        self.default_timeout = self.config.get_explicit_wait() * 1000  # Convert to milliseconds
    
    def wait_for_element_visible(self, selector: str, timeout: int = None) -> bool:
        """Wait for element to be visible"""
        timeout = timeout or self.default_timeout
        try:
            self.page.wait_for_selector(selector, state='visible', timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_element_hidden(self, selector: str, timeout: int = None) -> bool:
        """Wait for element to be hidden"""
        timeout = timeout or self.default_timeout
        try:
            self.page.wait_for_selector(selector, state='hidden', timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_element_clickable(self, selector: str, timeout: int = None) -> bool:
        """Wait for element to be clickable"""
        timeout = timeout or self.default_timeout
        try:
            element = self.page.locator(selector)
            element.wait_for(state='visible', timeout=timeout)
            expect(element).to_be_enabled(timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_text_present(self, text: str, timeout: int = None) -> bool:
        """Wait for text to be present on page"""
        timeout = timeout or self.default_timeout
        try:
            self.page.wait_for_selector(f"text={text}", timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_url_contains(self, url_part: str, timeout: int = None) -> bool:
        """Wait for URL to contain specific text"""
        timeout = timeout or self.default_timeout
        try:
            self.page.wait_for_url(f"**/*{url_part}*", timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_page_load(self, timeout: int = None) -> bool:
        """Wait for page to load completely"""
        timeout = timeout or self.default_timeout
        try:
            self.page.wait_for_load_state('networkidle', timeout=timeout)
            return True
        except Exception:
            return False
    
    def custom_wait(self, condition_func, timeout: int = None, poll_frequency: float = 0.5) -> bool:
        """Custom wait with user-defined condition"""
        timeout = timeout or self.default_timeout / 1000  # Convert back to seconds
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            try:
                if condition_func():
                    return True
            except Exception:
                pass
            time.sleep(poll_frequency)
        
        return False