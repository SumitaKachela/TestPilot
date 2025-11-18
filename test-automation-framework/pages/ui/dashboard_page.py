"""
Dashboard page object model
"""
from playwright.sync_api import Page
from pages.ui.base_page import BasePage

class DashboardPage(BasePage):
    """Dashboard page object with dashboard-specific functionality"""
    
    # Locators
    WELCOME_MESSAGE = ".welcome-message"
    USER_PROFILE = "#user-profile"
    LOGOUT_BUTTON = "#logout"
    NAVIGATION_MENU = ".nav-menu"
    DASHBOARD_TITLE = "h1"
    SIDEBAR = "#sidebar"
    MAIN_CONTENT = "#main-content"
    NOTIFICATIONS = ".notifications"
    SEARCH_BOX = "#search"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def get_welcome_message(self) -> str:
        """Get welcome message text"""
        self.wait_for_element(self.WELCOME_MESSAGE)
        return self.get_text(self.WELCOME_MESSAGE)
    
    def is_dashboard_loaded(self) -> bool:
        """Check if dashboard is loaded"""
        return self.is_element_visible(self.DASHBOARD_TITLE) and \
               self.is_element_visible(self.MAIN_CONTENT)
    
    def click_logout(self) -> None:
        """Click logout button"""
        self.logger.info("Clicking logout button")
        self.click_element(self.LOGOUT_BUTTON)
    
    def click_user_profile(self) -> None:
        """Click user profile"""
        self.logger.info("Clicking user profile")
        self.click_element(self.USER_PROFILE)
    
    def get_dashboard_title(self) -> str:
        """Get dashboard title"""
        return self.get_text(self.DASHBOARD_TITLE)
    
    def is_sidebar_visible(self) -> bool:
        """Check if sidebar is visible"""
        return self.is_element_visible(self.SIDEBAR)
    
    def search(self, search_term: str) -> None:
        """Perform search"""
        self.logger.info(f"Searching for: {search_term}")
        self.type_text(self.SEARCH_BOX, search_term)
        self.page.keyboard.press("Enter")
    
    def get_notifications_count(self) -> int:
        """Get number of notifications"""
        if self.is_element_visible(self.NOTIFICATIONS):
            notifications = self.page.locator(self.NOTIFICATIONS + " .notification-item")
            return notifications.count()
        return 0
    
    def navigate_to_section(self, section_name: str) -> None:
        """Navigate to specific section"""
        self.logger.info(f"Navigating to section: {section_name}")
        section_link = f"a[data-section='{section_name}']"
        self.click_element(section_link)