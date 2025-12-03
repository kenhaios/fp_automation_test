"""Welcome Page - First screen of the app"""

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from src.base.base_page import BasePage


class WelcomePage(BasePage):
    """Page object for the welcome/landing screen"""
    
    # Locators
    GET_STARTED_BUTTON = (AppiumBy.XPATH, "//*[@text='Get started' or @label='Get started' or @name='Get started']")
    WELCOME_MESSAGE = (AppiumBy.XPATH, "//*[@text='WELCOME TO FASTERPAY' or @label='WELCOME TO FASTERPAY']")
    SIGN_UP_BUTTON = (AppiumBy.XPATH, "//*[@text='Sign Up' or @label='Sign Up']")
    LOGIN_BUTTON = (AppiumBy.XPATH, "//*[@text='Login' or @label='Login']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: int = 30) -> None:
        """Wait for welcome page to load"""
        self.wait_and_assert_visible(self.GET_STARTED_BUTTON, timeout)
    
    def tap_get_started(self) -> None:
        """Tap the Get Started button"""
        self.tap(self.GET_STARTED_BUTTON)
    
    def tap_sign_up(self) -> None:
        """Tap the Sign Up button"""
        self.tap(self.SIGN_UP_BUTTON)
    
    def tap_login(self) -> None:
        """Tap the Login button"""
        self.tap(self.LOGIN_BUTTON)
    
    def is_welcome_message_visible(self) -> bool:
        """Check if welcome message is visible"""
        return self.is_element_visible(self.WELCOME_MESSAGE)
    
    def get_welcome_message_text(self) -> str:
        """Get the text of the welcome message"""
        return self.get_text(self.WELCOME_MESSAGE)
    
    def navigate_to_signup(self) -> None:
        """Navigate through welcome flow to signup"""
        self.tap_get_started()
        self.tap_sign_up()