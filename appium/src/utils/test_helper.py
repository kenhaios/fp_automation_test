"""Test helper utilities for common test operations"""

import time
import random
import string
from typing import Any, Dict


class TestHelper:
    """Utility class for common test helper functions"""
    
    @staticmethod
    def wait_with_timeout(condition_func, timeout: int = 30, poll_interval: float = 1.0) -> bool:
        """
        Wait for a condition to be true with timeout
        
        Args:
            condition_func: Function that returns True when condition is met
            timeout: Maximum wait time in seconds
            poll_interval: How often to check condition in seconds
            
        Returns:
            True if condition was met, False if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if condition_func():
                    return True
            except Exception:
                pass  # Ignore exceptions during condition checking
            time.sleep(poll_interval)
        return False
    
    @staticmethod
    def retry_on_exception(func, max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
        """
        Retry a function on exception
        
        Args:
            func: Function to retry
            max_attempts: Maximum number of attempts
            delay: Delay between attempts
            exceptions: Tuple of exceptions to catch
            
        Returns:
            Function result
            
        Raises:
            Last exception if all attempts fail
        """
        last_exception = None
        
        for attempt in range(max_attempts):
            try:
                return func()
            except exceptions as e:
                last_exception = e
                if attempt < max_attempts - 1:
                    time.sleep(delay)
                    continue
                break
        
        raise last_exception
    
    @staticmethod
    def generate_test_data() -> Dict[str, Any]:
        """
        Generate common test data
        
        Returns:
            Dictionary with test data
        """
        return {
            'email': TestHelper.generate_random_email(),
            'password': 'Test123@',
            'first_name': 'Test',
            'last_name': 'User',
            'address': TestHelper.generate_random_text(15),
            'postal_code': TestHelper.generate_random_digits(5),
            'city': TestHelper.generate_random_text(10)
        }
    
    @staticmethod
    def generate_random_email(domain: str = "test.com") -> str:
        """
        Generate random email address
        
        Args:
            domain: Email domain
            
        Returns:
            Random email address
        """
        username_length = random.randint(5, 10)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
        return f"{username}@{domain}"
    
    @staticmethod
    def generate_random_text(length: int = 10, include_numbers: bool = False) -> str:
        """
        Generate random text
        
        Args:
            length: Length of text to generate
            include_numbers: Whether to include numbers
            
        Returns:
            Random text string
        """
        chars = string.ascii_letters
        if include_numbers:
            chars += string.digits
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def generate_random_digits(length: int = 5) -> str:
        """
        Generate random digit string
        
        Args:
            length: Length of digit string
            
        Returns:
            Random digit string
        """
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def generate_random_password(length: int = 8, include_special: bool = True) -> str:
        """
        Generate random password
        
        Args:
            length: Password length
            include_special: Whether to include special characters
            
        Returns:
            Random password
        """
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += "!@#$%^&*"
        
        # Ensure at least one uppercase, lowercase, digit, and special char
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits)
        ]
        
        if include_special:
            password.append(random.choice("!@#$%^&*"))
        
        # Fill remaining length with random characters
        remaining_length = length - len(password)
        password.extend(random.choices(chars, k=remaining_length))
        
        # Shuffle to avoid predictable pattern
        random.shuffle(password)
        return ''.join(password)
    
    @staticmethod
    def format_test_result(test_name: str, status: str, duration: float, error: str = None) -> Dict[str, Any]:
        """
        Format test result for reporting
        
        Args:
            test_name: Name of the test
            status: Test status (PASS, FAIL, SKIP)
            duration: Test duration in seconds
            error: Error message if test failed
            
        Returns:
            Formatted test result
        """
        result = {
            'test_name': test_name,
            'status': status.upper(),
            'duration': round(duration, 2),
            'timestamp': time.time()
        }
        
        if error:
            result['error'] = error
        
        return result
    
    @staticmethod
    def take_screenshot_on_failure(driver, test_name: str) -> str:
        """
        Take screenshot on test failure
        
        Args:
            driver: WebDriver instance
            test_name: Name of the test
            
        Returns:
            Screenshot file path
        """
        timestamp = int(time.time())
        filename = f"screenshots/failure_{test_name}_{timestamp}.png"
        try:
            driver.save_screenshot(filename)
            return filename
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return ""
    
    @staticmethod
    def log_test_step(step_name: str, details: str = ""):
        """
        Log test step with timestamp
        
        Args:
            step_name: Name of the test step
            details: Additional details
        """
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        print(f"[{timestamp}] Step: {step_name}")
        if details:
            print(f"[{timestamp}] Details: {details}")
    
    @staticmethod
    def verify_element_attributes(element, expected_attributes: Dict[str, str]) -> bool:
        """
        Verify element attributes match expected values
        
        Args:
            element: WebElement to verify
            expected_attributes: Dictionary of attribute name -> expected value
            
        Returns:
            True if all attributes match, False otherwise
        """
        for attr_name, expected_value in expected_attributes.items():
            actual_value = element.get_attribute(attr_name)
            if actual_value != expected_value:
                print(f"Attribute mismatch: {attr_name} = '{actual_value}', expected '{expected_value}'")
                return False
        return True
    
    @staticmethod
    def compare_lists(actual: list, expected: list, ignore_order: bool = False) -> bool:
        """
        Compare two lists
        
        Args:
            actual: Actual list
            expected: Expected list
            ignore_order: Whether to ignore order when comparing
            
        Returns:
            True if lists match, False otherwise
        """
        if ignore_order:
            return sorted(actual) == sorted(expected)
        else:
            return actual == expected