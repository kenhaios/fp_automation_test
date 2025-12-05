"""Sign Up Page - Account type selection and phone number input"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from src.base.base_page import BasePage


class SignUpPage(BasePage):
    """Page object for the sign up screen"""
    
    # Account type locators - Multiple strategies for iOS UI structure
    ACCOUNT_TYPE_CONTAINER = (AppiumBy.XPATH, "//XCUIElementTypeScrollView | //XCUIElementTypeView")
    PERSONAL_TEXT = (AppiumBy.XPATH, "//*[@name='Personal' or @label='Personal' or contains(@name, 'Personal')]")
    BUSINESS_TEXT = (AppiumBy.XPATH, "//*[@name='Business' or @label='Business' or contains(@name, 'Business')]")
    
    # Container-based locators for account selection
    PERSONAL_CONTAINER = (AppiumBy.XPATH, "//XCUIElementTypeOther[descendant::*[@label='Personal' or @name='Personal']]")
    PERSONAL_CONTAINER_ALT = (AppiumBy.ACCESSIBILITY_ID, "itempersonal")
    BUSINESS_CONTAINER = (AppiumBy.XPATH, "//XCUIElementTypeOther[descendant::*[@label='Business' or @name='Business']]")
    
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
        # Wait for any text containing 'Personal' to appear (more reliable)
        strategies = [
            self.PERSONAL_TEXT,
            (AppiumBy.XPATH, "//*[contains(@label, 'Personal') or contains(@name, 'Personal')]"),
            (AppiumBy.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Personal')]"),
            self.ACCOUNT_TYPE_CONTAINER
        ]
        
        for strategy in strategies:
            try:
                self.wait_and_assert_visible(strategy, 10)
                print(f"✓ Page loaded - found element with strategy: {strategy}")
                return
            except Exception as e:
                print(f"Strategy {strategy} failed: {str(e)}")
                continue
        
        # If all strategies fail, take a screenshot for debugging
        self.take_screenshot("signup_page_load_failed")
        raise TimeoutException(f"Signup page did not load after {timeout} seconds")
    
    def select_personal_account(self) -> None:
        """Select Personal account type using multiple strategies"""
        print("Attempting to select Personal account...")
        
        # Strategy 1: Use the base page's iOS text finding method
        try:
            self.tap_by_text_ios("Personal", 10)
            print("✓ Personal account selected using tap_by_text_ios")
            return
        except Exception as e:
            print(f"Strategy 1 (tap_by_text_ios) failed: {str(e)}")
        
        # Strategy 2: Try container-based approach
        try:
            self.tap(self.PERSONAL_CONTAINER, 5)
            print("✓ Personal account selected using container locator")
            return
        except Exception as e:
            print(f"Strategy 2 (container) failed: {str(e)}")

        try:
            self.tap(self.PERSONAL_CONTAINER_ALT, 5)
            print("✓ Personal account selected using container locator alt")
            return
        except Exception as e:
            print(f"Strategy 2 (container alt) failed: {str(e)}")
        
        # Strategy 3: Try direct text element
        try:
            self.tap(self.PERSONAL_TEXT, 5)
            print("✓ Personal account selected using text locator")
            return
        except Exception as e:
            print(f"Strategy 3 (text) failed: {str(e)}")
        
        # Strategy 4: Comprehensive search and tap
        try:
            elements = self.find_elements_by_text_ios("Personal", 5)
            if elements:
                # Try each found element until one works
                for i, element in enumerate(elements):
                    try:
                        print(f"Trying element {i+1}/{len(elements)}...")
                        element.click()
                        print("✓ Personal account selected using comprehensive search")
                        return
                    except Exception as click_error:
                        print(f"Element {i+1} click failed: {str(click_error)}")
                        continue
        except Exception as e:
            print(f"Strategy 4 (comprehensive search) failed: {str(e)}")
        
        # If all strategies fail, take screenshot and raise error
        self.take_screenshot("personal_account_selection_failed")
        self._debug_page_elements()
        raise TimeoutException("Could not select Personal account with any strategy")
    
    def select_business_account(self) -> None:
        """Select Business account type using multiple strategies"""
        print("Attempting to select Business account...")
        
        # Strategy 1: Use the base page's iOS text finding method
        try:
            self.tap_by_text_ios("Business", 10)
            print("✓ Business account selected using tap_by_text_ios")
            return
        except Exception as e:
            print(f"Strategy 1 (tap_by_text_ios) failed: {str(e)}")
        
        # Strategy 2: Try container-based approach
        try:
            self.tap(self.BUSINESS_CONTAINER, 5)
            print("✓ Business account selected using container locator")
            return
        except Exception as e:
            print(f"Strategy 2 (container) failed: {str(e)}")
        
        # Strategy 3: Try direct text element
        try:
            self.tap(self.BUSINESS_TEXT, 5)
            print("✓ Business account selected using text locator")
            return
        except Exception as e:
            print(f"Strategy 3 (text) failed: {str(e)}")
        
        # If all strategies fail, take screenshot and raise error
        self.take_screenshot("business_account_selection_failed")
        self._debug_page_elements()
        raise TimeoutException("Could not select Business account with any strategy")
    
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
    
    def _debug_page_elements(self) -> None:
        """Debug method to print all visible elements on the page"""
        try:
            print("\n=== DEBUG: Page Elements ===")
            # Try to find all visible elements
            all_elements = self.driver.find_elements(AppiumBy.XPATH, "//*[@visible='true']")
            print(f"Found {len(all_elements)} visible elements")
            
            for i, element in enumerate(all_elements[:10]):  # Limit to first 10 elements
                try:
                    element_info = {
                        'index': i,
                        'tag_name': element.tag_name,
                        'name': element.get_attribute('name'),
                        'label': element.get_attribute('label'),
                        'value': element.get_attribute('value'),
                        'enabled': element.get_attribute('enabled'),
                        'visible': element.get_attribute('visible')
                    }
                    print(f"Element {i}: {element_info}")
                except Exception as e:
                    print(f"Could not get info for element {i}: {str(e)}")
            print("=== END DEBUG ===")
        except Exception as e:
            print(f"Debug failed: {str(e)}")