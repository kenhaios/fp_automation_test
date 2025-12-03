"""Personal Info Page - Email, password, name input"""

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from src.base.base_page import BasePage


class PersonalInfoPage(BasePage):
    """Page object for the personal information screen"""
    
    # Locators - OTP Field (appears first)
    OTP_FIELD = (AppiumBy.XPATH, "//*[contains(@resource-id,'otp') or contains(@accessibility-id,'otp')]")
    
    # Email section
    EMAIL_FIELD = (AppiumBy.ACCESSIBILITY_ID, "edtEmail")
    EMAIL_FIELD_ALT = (AppiumBy.ID, "edtEmail")
    CONTINUE_EMAIL_BUTTON = (AppiumBy.XPATH, "//*[@text='Continue' or @label='Continue']")
    
    # Password section
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "edtSignUpPassword")
    PASSWORD_FIELD_ALT = (AppiumBy.ID, "edtSignUpPassword")
    CONTINUE_PASSWORD_BUTTON = (AppiumBy.XPATH, "//*[@text='Continue' or @label='Continue']")
    
    # Name section
    FIRST_NAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "edtSignUpFirstName")
    FIRST_NAME_FIELD_ALT = (AppiumBy.ID, "edtSignUpFirstName")
    
    LAST_NAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "edtSignUpLastName")
    LAST_NAME_FIELD_ALT = (AppiumBy.ID, "edtSignUpLastName")
    
    CONTINUE_NAME_BUTTON = (AppiumBy.XPATH, "//*[@text='Continue' or @label='Continue']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def wait_for_otp_field(self, timeout: int = 30) -> None:
        """Wait for OTP field to be visible"""
        self.wait_and_assert_visible(self.OTP_FIELD, timeout)
    
    def enter_otp(self, otp_code: str) -> None:
        """
        Enter OTP verification code
        
        Args:
            otp_code: The OTP code to enter
        """
        self.input_text(self.OTP_FIELD, otp_code)
    
    def wait_for_email_field(self, timeout: int = 30) -> None:
        """Wait for email field to be visible"""
        try:
            self.wait_and_assert_visible(self.EMAIL_FIELD, timeout)
        except:
            self.wait_and_assert_visible(self.EMAIL_FIELD_ALT, timeout)
    
    def enter_email(self, email: str) -> None:
        """
        Enter email address
        
        Args:
            email: Email address to enter
        """
        try:
            self.input_text(self.EMAIL_FIELD, email)
        except:
            self.input_text(self.EMAIL_FIELD_ALT, email)
    
    def enter_random_email(self) -> str:
        """
        Enter a randomly generated email
        
        Returns:
            The generated email address
        """
        email = self.generate_random_email()
        self.enter_email(email)
        return email
    
    def tap_continue_after_email(self) -> None:
        """Tap continue button after entering email"""
        self.tap(self.CONTINUE_EMAIL_BUTTON)
    
    def wait_for_password_field(self, timeout: int = 30) -> None:
        """Wait for password field to be visible"""
        try:
            self.wait_and_assert_visible(self.PASSWORD_FIELD, timeout)
        except:
            self.wait_and_assert_visible(self.PASSWORD_FIELD_ALT, timeout)
    
    def enter_password(self, password: str) -> None:
        """
        Enter password
        
        Args:
            password: Password to enter
        """
        try:
            self.input_text(self.PASSWORD_FIELD, password)
        except:
            self.input_text(self.PASSWORD_FIELD_ALT, password)
    
    def tap_continue_after_password(self) -> None:
        """Tap continue button after entering password"""
        self.tap(self.CONTINUE_PASSWORD_BUTTON)
    
    def wait_for_name_fields(self, timeout: int = 30) -> None:
        """Wait for name fields to be visible"""
        try:
            self.wait_and_assert_visible(self.FIRST_NAME_FIELD, timeout)
        except:
            self.wait_and_assert_visible(self.FIRST_NAME_FIELD_ALT, timeout)
    
    def enter_first_name(self, first_name: str) -> None:
        """
        Enter first name
        
        Args:
            first_name: First name to enter
        """
        try:
            self.input_text(self.FIRST_NAME_FIELD, first_name)
        except:
            self.input_text(self.FIRST_NAME_FIELD_ALT, first_name)
    
    def enter_last_name(self, last_name: str) -> None:
        """
        Enter last name
        
        Args:
            last_name: Last name to enter
        """
        try:
            self.input_text(self.LAST_NAME_FIELD, last_name)
        except:
            self.input_text(self.LAST_NAME_FIELD_ALT, last_name)
    
    def tap_continue_after_name(self) -> None:
        """Tap continue button after entering names"""
        self.tap(self.CONTINUE_NAME_BUTTON)
    
    def complete_personal_info(self, otp_code: str, email: str = None, 
                             password: str = "12345Aa@", 
                             first_name: str = "Hellen", 
                             last_name: str = "Johnson") -> dict:
        """
        Complete all personal information steps
        
        Args:
            otp_code: OTP verification code
            email: Email (if None, random email will be generated)
            password: Password (default: "12345Aa@")
            first_name: First name (default: "Hellen")
            last_name: Last name (default: "Johnson")
            
        Returns:
            Dictionary with entered information
        """
        # Step 1: Enter OTP
        self.wait_for_otp_field()
        self.enter_otp(otp_code)
        
        # Step 2: Enter email
        self.wait_for_email_field()
        if email is None:
            email = self.enter_random_email()
        else:
            self.enter_email(email)
        self.tap_continue_after_email()
        
        # Step 3: Enter password
        self.wait_for_password_field()
        self.enter_password(password)
        self.tap_continue_after_password()
        
        # Step 4: Enter names
        self.wait_for_name_fields()
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.tap_continue_after_name()
        
        return {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }