"""
Base page class with common functionality for all page objects
"""
from playwright.sync_api import Page, expect
from utility.common.wait_helper import WaitHelper
from utility.common.logger import Logger

class BasePage:
    """Base page class containing common page operations"""
    
    def __init__(self, page: Page):
        self.page = page
        self.wait_helper = WaitHelper(page)
        self.logger = Logger().get_logger()
    
    def navigate_to(self, url: str) -> None:
        """Navigate to specified URL"""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.wait_helper.wait_for_page_load()
    
    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()
    
    def get_url(self) -> str:
        """Get current URL"""
        return self.page.url
    
    def click_element(self, selector: str) -> None:
        """Click on element"""
        self.logger.debug(f"Clicking element: {selector}")
        self.wait_helper.wait_for_element_clickable(selector)
        self.page.click(selector)
    
    def type_text(self, selector: str, text: str, clear_first: bool = True) -> None:
        """Type text into element"""
        self.logger.debug(f"Typing text into element: {selector}")
        self.wait_helper.wait_for_element_visible(selector)
        if clear_first:
            self.page.fill(selector, text)
        else:
            self.page.type(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Get text from element"""
        self.wait_helper.wait_for_element_visible(selector)
        return self.page.text_content(selector)
    
    def get_attribute(self, selector: str, attribute: str) -> str:
        """Get attribute value from element"""
        self.wait_helper.wait_for_element_visible(selector)
        return self.page.get_attribute(selector, attribute)
    
    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        try:
            return self.page.locator(selector).is_visible()
        except Exception:
            return False
    
    def is_element_enabled(self, selector: str) -> bool:
        """Check if element is enabled"""
        try:
            return self.page.locator(selector).is_enabled()
        except Exception:
            return False
    
    def wait_for_element(self, selector: str, timeout: int = None) -> bool:
        """Wait for element to be visible"""
        return self.wait_helper.wait_for_element_visible(selector, timeout)
    
    def scroll_to_element(self, selector: str) -> None:
        """Scroll to element"""
        self.page.locator(selector).scroll_into_view_if_needed()
    
    def select_dropdown_option(self, selector: str, option_value: str) -> None:
        """Select option from dropdown"""
        self.logger.debug(f"Selecting dropdown option: {option_value}")
        self.page.select_option(selector, option_value)
    
    def upload_file(self, selector: str, file_path: str) -> None:
        """Upload file"""
        self.logger.debug(f"Uploading file: {file_path}")
        self.page.set_input_files(selector, file_path)
    
    def switch_to_frame(self, frame_selector: str) -> None:
        """Switch to iframe"""
        frame = self.page.frame_locator(frame_selector)
        return frame
    
    def accept_alert(self) -> None:
        """Accept JavaScript alert"""
        self.page.on("dialog", lambda dialog: dialog.accept())
    
    def dismiss_alert(self) -> None:
        """Dismiss JavaScript alert"""
        self.page.on("dialog", lambda dialog: dialog.dismiss())
    
    def refresh_page(self) -> None:
        """Refresh current page"""
        self.logger.info("Refreshing page")
        self.page.reload()
        self.wait_helper.wait_for_page_load()
    
    def go_back(self) -> None:
        """Navigate back"""
        self.page.go_back()
        self.wait_helper.wait_for_page_load()
    
    def verify_text_present(self, text: str) -> bool:
        """Verify text is present on page"""
        try:
            expect(self.page.locator(f"text={text}")).to_be_visible()
            return True
        except Exception:
            return False
    
    def verify_element_present(self, selector: str) -> bool:
        """Verify element is present"""
        try:
            expect(self.page.locator(selector)).to_be_visible()
            return True
        except Exception:
            return False