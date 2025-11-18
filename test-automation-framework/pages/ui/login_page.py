"""
Login page object model
"""
from playwright.sync_api import Page
from pages.ui.base_page import BasePage

class LoginPage(BasePage):
    """Login page object with login-specific functionality"""
    
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = ".error-message"
    FORGOT_PASSWORD_LINK = "#forgot-password"
    REMEMBER_ME_CHECKBOX = "#remember-me"
    LOGIN_FORM = "#login-form"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def enter_username(self, username: str) -> None:
        """Enter username"""
        self.logger.info(f"Entering username: {username}")
        self.type_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """Enter password"""
        self.logger.info("Entering password")
        self.type_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """Click login button"""
        self.logger.info("Clicking login button")
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> None:
        """Complete login process"""
        self.logger.info(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def click_forgot_password(self) -> None:
        """Click forgot password link"""
        self.logger.info("Clicking forgot password link")
        self.click_element(self.FORGOT_PASSWORD_LINK)
    
    def check_remember_me(self) -> None:
        """Check remember me checkbox"""
        self.logger.info("Checking remember me checkbox")
        if not self.page.is_checked(self.REMEMBER_ME_CHECKBOX):
            self.click_element(self.REMEMBER_ME_CHECKBOX)
    
    def uncheck_remember_me(self) -> None:
        """Uncheck remember me checkbox"""
        self.logger.info("Unchecking remember me checkbox")
        if self.page.is_checked(self.REMEMBER_ME_CHECKBOX):
            self.click_element(self.REMEMBER_ME_CHECKBOX)
    
    def is_login_form_displayed(self) -> bool:
        """Check if login form is displayed"""
        return self.is_element_visible(self.LOGIN_FORM)
    
    def clear_username(self) -> None:
        """Clear username field"""
        self.page.fill(self.USERNAME_INPUT, "")
    
    def clear_password(self) -> None:
        """Clear password field"""
        self.page.fill(self.PASSWORD_INPUT, "")
    
    def get_username_placeholder(self) -> str:
        """Get username field placeholder text"""
        return self.get_attribute(self.USERNAME_INPUT, "placeholder")
    
    def get_password_placeholder(self) -> str:
        """Get password field placeholder text"""
        return self.get_attribute(self.PASSWORD_INPUT, "placeholder")
    
    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled"""
        return self.is_element_enabled(self.LOGIN_BUTTON)