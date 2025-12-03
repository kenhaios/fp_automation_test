"""Phone number generation utility - ported from Maestro JavaScript"""

import random


class PhoneGenerator:
    """Utility class for generating random phone numbers"""
    
    @staticmethod
    def generate_random_phone() -> str:
        """
        Generate random 10-digit phone number
        First digit: 1-9, remaining digits: 0-9
        
        Returns:
            String representation of 10-digit phone number
        """
        # First digit must be 1-9
        first_digit = random.randint(1, 9)
        
        # Remaining 9 digits can be 0-9
        rest_digits = [str(random.randint(0, 9)) for _ in range(9)]
        
        return str(first_digit) + ''.join(rest_digits)
    
    @staticmethod
    def generate_phone_with_area_code(area_code: str = "555") -> str:
        """
        Generate phone number with specific area code
        
        Args:
            area_code: 3-digit area code (default: "555")
            
        Returns:
            Phone number in format: area_code + 7 digits
        """
        if len(area_code) != 3:
            raise ValueError("Area code must be 3 digits")
        
        # Generate 7 remaining digits
        remaining_digits = [str(random.randint(0, 9)) for _ in range(7)]
        
        return area_code + ''.join(remaining_digits)
    
    @staticmethod
    def format_phone_number(phone: str, format_type: str = "raw") -> str:
        """
        Format phone number according to specified format
        
        Args:
            phone: Raw phone number string
            format_type: "raw", "dashes", "parentheses", "international"
            
        Returns:
            Formatted phone number
        """
        if len(phone) != 10:
            raise ValueError("Phone number must be 10 digits")
        
        if format_type == "raw":
            return phone
        elif format_type == "dashes":
            return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        elif format_type == "parentheses":
            return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
        elif format_type == "international":
            return f"+1-{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """
        Validate phone number format
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Remove non-digit characters
        digits_only = ''.join(filter(str.isdigit, phone))
        
        # Check if it's 10 digits and first digit is not 0
        if len(digits_only) == 10 and digits_only[0] != '0':
            return True
        
        return False


# Convenience function for direct usage (similar to Maestro script)
def generate_phone() -> str:
    """
    Generate a random phone number (convenience function)
    
    Returns:
        10-digit phone number as string
    """
    return PhoneGenerator.generate_random_phone()


# For compatibility with test data structures
def get_generated_phone() -> dict:
    """
    Generate phone number and return in dictionary format
    (compatible with original Maestro output format)
    
    Returns:
        Dictionary with 'generatedPhone' key
    """
    phone = PhoneGenerator.generate_random_phone()
    return {"generatedPhone": phone}