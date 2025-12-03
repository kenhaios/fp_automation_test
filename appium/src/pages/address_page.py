"""Address Page - Address information input"""

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from src.base.base_page import BasePage


class AddressPage(BasePage):
    """Page object for the address information screen"""
    
    # Locators
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "btnContinue")
    CONTINUE_BUTTON_ALT = (AppiumBy.ID, "btnContinue")
    
    # Address fields (using text-based locators since they might be generic input fields)
    ADDRESS_FIELD = (AppiumBy.XPATH, "//*[@text='Address' or @hint='Address' or @content-desc='Address']")
    POSTAL_CODE_FIELD = (AppiumBy.XPATH, "//*[@text='Postal Code' or @hint='Postal Code' or @content-desc='Postal Code']")
    CITY_FIELD = (AppiumBy.XPATH, "//*[@text='City' or @hint='City' or @content-desc='City']")
    STATE_FIELD = (AppiumBy.XPATH, "//*[@text='State' or @hint='State' or @content-desc='State']")
    
    # State selection
    ALASKA_STATE = (AppiumBy.XPATH, "//*[@text='Alaska' or @label='Alaska']")
    
    # Localization continue button (might be different from main continue)
    LOCALIZATION_CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "btnLocalizationContinue")
    LOCALIZATION_CONTINUE_BUTTON_ALT = (AppiumBy.ID, "btnLocalizationContinue")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: int = 30) -> None:
        """Wait for address page to load"""
        try:
            self.wait_and_assert_visible(self.CONTINUE_BUTTON, timeout)
        except:
            self.wait_and_assert_visible(self.CONTINUE_BUTTON_ALT, timeout)
    
    def tap_continue(self) -> None:
        """Tap the main continue button"""
        try:
            self.tap(self.CONTINUE_BUTTON)
        except:
            self.tap(self.CONTINUE_BUTTON_ALT)
    
    def tap_address_field(self) -> None:
        """Tap on address field"""
        self.tap(self.ADDRESS_FIELD)
    
    def enter_address(self, address: str) -> None:
        """
        Enter address information
        
        Args:
            address: Address to enter
        """
        self.tap_address_field()
        self.input_text(self.ADDRESS_FIELD, address)
    
    def enter_random_address(self, length: int = 10) -> str:
        """
        Enter random address text
        
        Args:
            length: Length of random address
            
        Returns:
            Generated address text
        """
        address = self.generate_random_text(length)
        self.enter_address(address)
        return address
    
    def tap_postal_code_field(self) -> None:
        """Tap on postal code field"""
        self.tap(self.POSTAL_CODE_FIELD)
    
    def enter_postal_code(self, postal_code: str) -> None:
        """
        Enter postal code
        
        Args:
            postal_code: Postal code to enter
        """
        self.tap_postal_code_field()
        self.input_text(self.POSTAL_CODE_FIELD, postal_code)
    
    def enter_random_postal_code(self, length: int = 5) -> str:
        """
        Enter random postal code
        
        Args:
            length: Length of postal code
            
        Returns:
            Generated postal code
        """
        postal_code = self.generate_random_number(length)
        self.enter_postal_code(postal_code)
        return postal_code
    
    def tap_city_field(self) -> None:
        """Tap on city field"""
        self.tap(self.CITY_FIELD)
    
    def enter_city(self, city: str) -> None:
        """
        Enter city name
        
        Args:
            city: City name to enter
        """
        self.tap_city_field()
        self.input_text(self.CITY_FIELD, city)
    
    def enter_random_city(self, length: int = 10) -> str:
        """
        Enter random city name
        
        Args:
            length: Length of city name
            
        Returns:
            Generated city name
        """
        city = self.generate_random_text(length)
        self.enter_city(city)
        return city
    
    def tap_state_field(self) -> None:
        """Tap on state field"""
        self.tap(self.STATE_FIELD)
    
    def select_alaska_state(self) -> None:
        """Select Alaska as the state"""
        self.tap_state_field()
        self.tap(self.ALASKA_STATE)
    
    def tap_localization_continue(self) -> None:
        """Tap the localization continue button"""
        try:
            self.tap(self.LOCALIZATION_CONTINUE_BUTTON)
        except:
            self.tap(self.LOCALIZATION_CONTINUE_BUTTON_ALT)
    
    def complete_address_info(self, address: str = None, postal_code: str = None, 
                            city: str = None, state: str = "Alaska") -> dict:
        """
        Complete all address information
        
        Args:
            address: Address (if None, random will be generated)
            postal_code: Postal code (if None, random will be generated)
            city: City (if None, random will be generated)
            state: State selection (default: "Alaska")
            
        Returns:
            Dictionary with entered address information
        """
        # First tap continue to proceed to address form
        self.tap_continue()
        
        # Enter address information
        if address is None:
            address = self.enter_random_address(10)
        else:
            self.enter_address(address)
        
        if postal_code is None:
            postal_code = self.enter_random_postal_code(5)
        else:
            self.enter_postal_code(postal_code)
        
        if city is None:
            city = self.enter_random_city(10)
        else:
            self.enter_city(city)
        
        # Select state (currently only supports Alaska)
        if state == "Alaska":
            self.select_alaska_state()
        
        # Complete address form
        self.tap_localization_continue()
        
        return {
            "address": address,
            "postal_code": postal_code,
            "city": city,
            "state": state
        }
    
    def is_address_field_visible(self) -> bool:
        """Check if address field is visible"""
        return self.is_element_visible(self.ADDRESS_FIELD, 2)
    
    def is_continue_button_visible(self) -> bool:
        """Check if continue button is visible"""
        return (self.is_element_visible(self.CONTINUE_BUTTON, 2) or 
                self.is_element_visible(self.CONTINUE_BUTTON_ALT, 2))