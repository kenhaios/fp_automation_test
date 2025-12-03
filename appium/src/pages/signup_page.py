"""Sign Up Page - Account type selection and phone number input"""

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from src.base.base_page import BasePage


class SignUpPage(BasePage):
    """Page object for the sign up screen"""
    
    # Locators
    PERSONAL_BUTTON = (AppiumBy.XPATH, "//*[@text='Personal' or @label='Personal']")
    BUSINESS_BUTTON = (AppiumBy.XPATH, "//*[@text='Business' or @label='Business']")
    
    PHONE_NUMBER_FIELD = (AppiumBy.ACCESSIBILITY_ID, "edtPhoneNumber")
    PHONE_NUMBER_FIELD_ALT = (AppiumBy.ID, "edtPhoneNumber")
    
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "btnContinue")
    CONTINUE_BUTTON_ALT = (AppiumBy.ID, "btnContinue")
    
    OTP_EMAIL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "otpViewEmail")
    OTP_EMAIL_BUTTON_ALT = (AppiumBy.ID, "otpViewEmail")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: int = 30) -> None:
        """Wait for sign up page to load"""
        self.wait_and_assert_visible(self.PERSONAL_BUTTON, timeout)
    
    def select_personal_account(self) -> None:
        """Select Personal account type"""
        self.tap(self.PERSONAL_BUTTON)
    
    def select_business_account(self) -> None:
        """Select Business account type"""
        self.tap(self.BUSINESS_BUTTON)
    
    def enter_phone_number(self, phone_number: str) -> None:
        """
        Enter phone number in the phone number field
        
        Args:
            phone_number: Phone number to enter
        """
        try:
            # Try accessibility ID first
            self.input_text(self.PHONE_NUMBER_FIELD, phone_number)
        except:
            # Fallback to resource ID
            self.input_text(self.PHONE_NUMBER_FIELD_ALT, phone_number)
    
    def get_phone_number(self) -> str:
        """
        Get the phone number from the field
        
        Returns:
            Phone number text
        """
        try:
            return self.get_text(self.PHONE_NUMBER_FIELD)
        except:
            return self.get_text(self.PHONE_NUMBER_FIELD_ALT)
    
    def tap_continue(self) -> None:
        """Tap the Continue button"""
        try:
            self.tap(self.CONTINUE_BUTTON)
        except:
            self.tap(self.CONTINUE_BUTTON_ALT)
    
    def tap_otp_email_option(self) -> None:
        """Tap the OTP via email option"""
        try:
            self.tap(self.OTP_EMAIL_BUTTON)
        except:
            self.tap(self.OTP_EMAIL_BUTTON_ALT)
    
    def complete_phone_verification_setup(self, phone_number: str) -> str:
        """
        Complete the phone verification setup process
        
        Args:
            phone_number: Phone number to enter
            
        Returns:
            The entered phone number for verification
        """
        self.select_personal_account()
        self.enter_phone_number(phone_number)
        
        # Get the entered phone number for later use
        entered_phone = self.get_phone_number()
        
        self.tap_continue()
        self.tap_otp_email_option()
        
        return entered_phone
    
    def is_phone_field_visible(self) -> bool:
        """Check if phone number field is visible"""
        return (self.is_element_visible(self.PHONE_NUMBER_FIELD, 2) or 
                self.is_element_visible(self.PHONE_NUMBER_FIELD_ALT, 2))
    
    def is_continue_button_enabled(self) -> bool:
        """Check if continue button is enabled"""
        try:
            element = self.find_element(self.CONTINUE_BUTTON, 2)
            return element.is_enabled()
        except:
            try:
                element = self.find_element(self.CONTINUE_BUTTON_ALT, 2)
                return element.is_enabled()
            except:
                return False