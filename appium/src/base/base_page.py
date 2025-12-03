"""Base Page class with common WebDriver functionality"""

import time
from typing import List, Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy


class BasePage:
    """Base page class containing common functionality for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 30)
    
    # Element interaction methods
    def find_element(self, locator: Tuple[By, str], timeout: int = 10) -> WebElement:
        """Find element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator: Tuple[By, str], timeout: int = 10) -> List[WebElement]:
        """Find multiple elements with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)
    
    def is_element_present(self, locator: Tuple[By, str], timeout: int = 5) -> bool:
        """Check if element is present"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Tuple[By, str], timeout: int = 5) -> bool:
        """Check if element is visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_clickable(self, locator: Tuple[By, str], timeout: int = 10) -> WebElement:
        """Wait for element to be clickable"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    # Tap/Click methods
    def tap(self, locator: Tuple[By, str], timeout: int = 10) -> None:
        """Tap on element"""
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    def tap_by_text(self, text: str, timeout: int = 10) -> None:
        """Tap element by text content"""
        locator = (AppiumBy.XPATH, f"//*[@text='{text}' or @label='{text}' or @name='{text}']")
        self.tap(locator, timeout)
    
    def tap_by_id(self, element_id: str, timeout: int = 10) -> None:
        """Tap element by accessibility id or resource id"""
        # Try accessibility id first, then resource id for Android
        try:
            locator = (AppiumBy.ACCESSIBILITY_ID, element_id)
            self.tap(locator, timeout)
        except TimeoutException:
            # Try resource id for Android
            locator = (AppiumBy.ID, element_id)
            self.tap(locator, timeout)
    
    # Input methods
    def input_text(self, locator: Tuple[By, str], text: str, timeout: int = 10) -> None:
        """Input text into element"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def input_text_by_id(self, element_id: str, text: str, timeout: int = 10) -> None:
        """Input text by accessibility id or resource id"""
        try:
            locator = (AppiumBy.ACCESSIBILITY_ID, element_id)
            self.input_text(locator, text, timeout)
        except TimeoutException:
            locator = (AppiumBy.ID, element_id)
            self.input_text(locator, text, timeout)
    
    def get_text(self, locator: Tuple[By, str], timeout: int = 10) -> str:
        """Get text from element"""
        element = self.find_element(locator, timeout)
        return element.text or element.get_attribute("label") or element.get_attribute("name") or ""
    
    # Scroll methods
    def scroll_to_element(self, locator: Tuple[By, str], max_scrolls: int = 5) -> bool:
        """Scroll until element is visible"""
        for _ in range(max_scrolls):
            if self.is_element_visible(locator, 2):
                return True
            self.scroll_down()
        return False
    
    def scroll_down(self) -> None:
        """Scroll down"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 3 // 4
        end_x = start_x
        end_y = size['height'] // 4
        self.driver.swipe(start_x, start_y, end_x, end_y, 500)
    
    def scroll_up(self) -> None:
        """Scroll up"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] // 4
        end_x = start_x
        end_y = size['height'] * 3 // 4
        self.driver.swipe(start_x, start_y, end_x, end_y, 500)
    
    def scroll_until_visible(self, locator: Tuple[By, str], max_attempts: int = 5) -> bool:
        """Scroll until element becomes visible"""
        for attempt in range(max_attempts):
            if self.is_element_visible(locator, 2):
                return True
            if attempt < max_attempts - 1:  # Don't scroll on last attempt
                self.scroll_down()
        return False
    
    # Wait methods
    def wait_for_page_load(self, timeout: int = 30) -> None:
        """Wait for page to load (override in specific pages)"""
        time.sleep(1)  # Basic implementation
    
    def wait_and_assert_visible(self, locator: Tuple[By, str], timeout: int = 10) -> None:
        """Wait for element and assert it's visible"""
        if not self.is_element_visible(locator, timeout):
            raise AssertionError(f"Element {locator} is not visible after {timeout} seconds")
    
    # Utility methods
    def take_screenshot(self, name: str) -> str:
        """Take screenshot and return filepath"""
        timestamp = int(time.time())
        filename = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        return filename
    
    def get_current_activity(self) -> Optional[str]:
        """Get current activity (Android only)"""
        try:
            return self.driver.current_activity
        except:
            return None
    
    def hide_keyboard(self) -> None:
        """Hide keyboard if present"""
        try:
            self.driver.hide_keyboard()
        except:
            pass  # Keyboard might not be present
    
    # Random input generators
    def generate_random_email(self) -> str:
        """Generate random email address"""
        import random
        import string
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = random.choice(['test.com', 'example.org', 'demo.net'])
        return f"{username}@{domain}"
    
    def generate_random_text(self, length: int = 10) -> str:
        """Generate random text"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def generate_random_number(self, length: int = 5) -> str:
        """Generate random number string"""
        import random
        import string
        return ''.join(random.choices(string.digits, k=length))