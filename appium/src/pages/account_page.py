"""Account Page - Final account verification and logout"""

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from src.base.base_page import BasePage


class AccountPage(BasePage):
    """Page object for the account/dashboard screen"""
    
    # Locators - Main account elements
    ACCOUNT_TEXT = (AppiumBy.XPATH, "//*[@text='ACCOUNT' or @label='ACCOUNT']")
    ADD_MONEY_TEXT = (AppiumBy.XPATH, "//*[@text='Add money' or @label='Add money']")
    
    # Settings and logout
    SETTINGS_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "imgSetting")
    SETTINGS_BUTTON_ALT = (AppiumBy.ID, "imgSetting")
    
    LOGOUT_BUTTON = (AppiumBy.XPATH, "//*[@text='Log out' or @label='Log out']")
    OK_BUTTON = (AppiumBy.XPATH, "//*[@text='OK' or @label='OK']")
    
    # Welcome message (after logout)
    WELCOME_MESSAGE = (AppiumBy.XPATH, "//*[@text='WELCOME TO FASTERPAY' or @label='WELCOME TO FASTERPAY']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: int = 30) -> None:
        """Wait for account page to load"""
        self.wait_and_assert_visible(self.ACCOUNT_TEXT, timeout)
    
    def is_account_visible(self) -> bool:
        """Check if ACCOUNT text is visible"""
        return self.is_element_visible(self.ACCOUNT_TEXT)
    
    def is_add_money_visible(self) -> bool:
        """Check if 'Add money' text is visible"""
        return self.is_element_visible(self.ADD_MONEY_TEXT)
    
    def verify_account_elements(self) -> bool:
        """
        Verify that key account elements are visible
        
        Returns:
            True if all key elements are visible
        """
        return self.is_account_visible() and self.is_add_money_visible()
    
    def tap_settings(self) -> None:
        """Tap the settings button"""
        try:
            self.tap(self.SETTINGS_BUTTON)
        except:
            self.tap(self.SETTINGS_BUTTON_ALT)
    
    def scroll_to_logout(self) -> None:
        """Scroll until logout button is visible"""
        self.scroll_until_visible(self.LOGOUT_BUTTON, max_attempts=5)
    
    def tap_logout(self) -> None:
        """Tap the logout button"""
        self.tap(self.LOGOUT_BUTTON)
    
    def confirm_logout(self) -> None:
        """Confirm logout by tapping OK"""
        self.tap(self.OK_BUTTON)
    
    def verify_logout_success(self) -> bool:
        """
        Verify that logout was successful by checking for welcome message
        
        Returns:
            True if welcome message is visible (indicating successful logout)
        """
        return self.is_element_visible(self.WELCOME_MESSAGE, timeout=10)
    
    def perform_logout_flow(self) -> bool:
        """
        Perform complete logout flow and verify success
        
        Returns:
            True if logout was successful
        """
        # Navigate to settings
        self.tap_settings()
        
        # Scroll to find logout button
        self.scroll_to_logout()
        
        # Perform logout
        self.tap_logout()
        self.confirm_logout()
        
        # Verify logout success
        return self.verify_logout_success()
    
    def get_account_text(self) -> str:
        """Get the account text"""
        return self.get_text(self.ACCOUNT_TEXT)
    
    def get_add_money_text(self) -> str:
        """Get the add money text"""
        return self.get_text(self.ADD_MONEY_TEXT)
    
    def take_account_screenshot(self) -> str:
        """Take screenshot of account page"""
        return self.take_screenshot("account_page")
    
    def assert_account_page_loaded(self) -> None:
        """Assert that account page has loaded successfully"""
        assert self.is_account_visible(), "ACCOUNT text is not visible"
        assert self.is_add_money_visible(), "Add money text is not visible"
    
    def get_page_elements_info(self) -> dict:
        """
        Get information about visible page elements
        
        Returns:
            Dictionary with element visibility status
        """
        return {
            "account_visible": self.is_account_visible(),
            "add_money_visible": self.is_add_money_visible(),
            "settings_visible": (self.is_element_visible(self.SETTINGS_BUTTON, 2) or 
                               self.is_element_visible(self.SETTINGS_BUTTON_ALT, 2))
        }