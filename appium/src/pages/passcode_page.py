"""Passcode Page - Date of birth and passcode setup"""

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from src.base.base_page import BasePage


class PasscodePage(BasePage):
    """Page object for the passcode and DOB setup screen"""
    
    # Locators
    DOB_CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "btnSignUpDOBContinue")
    DOB_CONTINUE_BUTTON_ALT = (AppiumBy.ID, "btnSignUpDOBContinue")
    
    SKIP_BUTTON = (AppiumBy.XPATH, "//*[@text='Skip' or @label='Skip']")
    DO_IT_LATER_BUTTON = (AppiumBy.XPATH, "//*[@text='Do it later' or @label='Do it later']")
    
    # Passcode view
    PASSCODE_VIEW = (AppiumBy.ACCESSIBILITY_ID, "rvPasscodeView")
    PASSCODE_VIEW_ALT = (AppiumBy.ID, "rvPasscodeView")
    
    # Number buttons (0-9)
    NUMBER_0 = (AppiumBy.XPATH, "//*[@text='0' or @label='0']")
    NUMBER_1 = (AppiumBy.XPATH, "//*[@text='1' or @label='1']")
    NUMBER_2 = (AppiumBy.XPATH, "//*[@text='2' or @label='2']")
    NUMBER_3 = (AppiumBy.XPATH, "//*[@text='3' or @label='3']")
    NUMBER_4 = (AppiumBy.XPATH, "//*[@text='4' or @label='4']")
    NUMBER_5 = (AppiumBy.XPATH, "//*[@text='5' or @label='5']")
    NUMBER_6 = (AppiumBy.XPATH, "//*[@text='6' or @label='6']")
    NUMBER_7 = (AppiumBy.XPATH, "//*[@text='7' or @label='7']")
    NUMBER_8 = (AppiumBy.XPATH, "//*[@text='8' or @label='8']")
    NUMBER_9 = (AppiumBy.XPATH, "//*[@text='9' or @label='9']")
    
    # Generic button for additional screens
    BUTTON_7 = (AppiumBy.ACCESSIBILITY_ID, "button7")
    BUTTON_7_ALT = (AppiumBy.ID, "button7")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: int = 30) -> None:
        """Wait for passcode page to load"""
        try:
            self.wait_and_assert_visible(self.DOB_CONTINUE_BUTTON, timeout)
        except:
            self.wait_and_assert_visible(self.DOB_CONTINUE_BUTTON_ALT, timeout)
    
    def tap_dob_continue(self) -> None:
        """Tap the DOB continue button"""
        try:
            self.tap(self.DOB_CONTINUE_BUTTON)
        except:
            self.tap(self.DOB_CONTINUE_BUTTON_ALT)
    
    def tap_skip(self) -> None:
        """Tap the Skip button"""
        self.tap(self.SKIP_BUTTON)
    
    def wait_for_passcode_view(self, timeout: int = 30) -> None:
        """Wait for passcode view to be visible"""
        try:
            self.wait_and_assert_visible(self.PASSCODE_VIEW, timeout)
        except:
            self.wait_and_assert_visible(self.PASSCODE_VIEW_ALT, timeout)
    
    def tap_number(self, number: str) -> None:
        """
        Tap a specific number on the passcode pad
        
        Args:
            number: Number to tap (0-9)
        """
        number_locators = {
            "0": self.NUMBER_0,
            "1": self.NUMBER_1,
            "2": self.NUMBER_2,
            "3": self.NUMBER_3,
            "4": self.NUMBER_4,
            "5": self.NUMBER_5,
            "6": self.NUMBER_6,
            "7": self.NUMBER_7,
            "8": self.NUMBER_8,
            "9": self.NUMBER_9
        }
        
        if number in number_locators:
            self.tap(number_locators[number])
        else:
            raise ValueError(f"Invalid number: {number}. Must be 0-9.")
    
    def enter_passcode_sequence(self, passcode: str, repeat_count: int = 1) -> None:
        """
        Enter a passcode sequence
        
        Args:
            passcode: Passcode to enter (e.g., "000000")
            repeat_count: How many times to repeat the sequence
        """
        for _ in range(repeat_count):
            for digit in passcode:
                self.tap_number(digit)
                # Add delay between taps as specified in original Maestro test
                import time
                time.sleep(0.5)
    
    def enter_six_zeros(self) -> None:
        """Enter six zeros as passcode (matches Maestro test)"""
        self.enter_passcode_sequence("000000")
    
    def confirm_passcode_with_six_zeros(self) -> None:
        """Enter passcode confirmation with six zeros"""
        self.enter_passcode_sequence("000000")
    
    def tap_do_it_later(self) -> None:
        """Tap the 'Do it later' button"""
        self.tap(self.DO_IT_LATER_BUTTON)
    
    def tap_button_7_if_present(self) -> None:
        """Tap button7 if it's present (optional step)"""
        try:
            if self.is_element_visible(self.BUTTON_7, 2):
                self.tap(self.BUTTON_7)
            elif self.is_element_visible(self.BUTTON_7_ALT, 2):
                self.tap(self.BUTTON_7_ALT)
        except:
            # Button not present, continue
            pass
    
    def complete_passcode_setup(self, passcode: str = "000000", skip_dob: bool = True) -> dict:
        """
        Complete the entire passcode setup process
        
        Args:
            passcode: Passcode to set (default: "000000")
            skip_dob: Whether to skip date of birth (default: True)
            
        Returns:
            Dictionary with setup information
        """
        # Handle DOB section
        self.tap_dob_continue()
        
        if skip_dob:
            self.tap_skip()
        
        # Enter passcode (first time)
        self.wait_for_passcode_view()
        self.enter_passcode_sequence(passcode)
        
        # Confirm passcode (second time)
        self.wait_for_passcode_view()
        self.enter_passcode_sequence(passcode)
        
        # Handle "Do it later" option
        self.tap_do_it_later()
        
        # Handle optional button7 (if present)
        self.tap_button_7_if_present()
        
        return {
            "passcode": passcode,
            "dob_skipped": skip_dob
        }
    
    def is_passcode_view_visible(self) -> bool:
        """Check if passcode view is visible"""
        return (self.is_element_visible(self.PASSCODE_VIEW, 2) or 
                self.is_element_visible(self.PASSCODE_VIEW_ALT, 2))
    
    def is_skip_button_visible(self) -> bool:
        """Check if skip button is visible"""
        return self.is_element_visible(self.SKIP_BUTTON, 2)