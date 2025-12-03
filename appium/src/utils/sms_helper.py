"""SMS helper utilities for Appium tests - ported from Maestro JavaScript"""

import re
import time
import requests
from typing import Optional, Dict, List, Any


class SMSHelper:
    """Utility class for SMS verification code retrieval"""
    
    def __init__(self, base_url: str = "http://mail.bamboo.stuffio.com/api/v2"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'mail.bamboo.stuffio.com'
        })
    
    def clean_sms_body(self, body: str) -> str:
        """
        Clean and normalize SMS body to handle encoding artifacts
        
        Args:
            body: Raw SMS body content
            
        Returns:
            Cleaned SMS body
        """
        if not body:
            return ''
        
        print(f'Cleaning SMS body - Original length: {len(body)}')
        
        # Remove carriage returns and newlines
        cleaned = body.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
        print(f'After removing line breaks: {cleaned}')
        
        # Handle quoted-printable encoding
        cleaned = re.sub(r'=\s', '', cleaned)
        print(f'After removing quoted-printable artifacts: {cleaned}')
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        print(f'After normalizing whitespace: {cleaned}')
        
        return cleaned
    
    def extract_verification_code(self, cleaned_body: str) -> Optional[str]:
        """
        Extract verification code from cleaned SMS body using multiple strategies
        
        Args:
            cleaned_body: The cleaned SMS body content
            
        Returns:
            The extracted verification code or None if not found
        """
        if not cleaned_body:
            return None
        
        print(f'Extracting verification code from: {cleaned_body}')
        
        # Strategy 1: Look for 6 consecutive digits
        match = re.search(r'\b\d{6}\b', cleaned_body)
        if match:
            code = match.group(0)
            print(f'Strategy 1 (6 consecutive digits) found: {code}')
            return code
        
        # Strategy 2: Look for 5-7 digits
        match = re.search(r'\b\d{5,7}\b', cleaned_body)
        if match:
            code = match.group(0)
            print(f'Strategy 2 (5-7 digits) found: {code}')
            if len(code) == 6:
                return code
            elif len(code) > 6:
                truncated = code[:6]
                print(f'Code too long, taking first 6 digits: {truncated}')
                return truncated
            else:
                print(f'Code shorter than 6 digits, using as-is: {code}')
                return code
        
        # Strategy 3: Look for digits around "verification code" keywords
        match = re.search(r'(?:verification\s+code|code)\s*:?\s*(\d{4,8})', cleaned_body, re.IGNORECASE)
        if match:
            code = match.group(1)
            print(f'Strategy 3 (context-based) found: {code}')
            return code
        
        # Strategy 4: Look for any sequence of 4-8 digits
        match = re.search(r'\d{4,8}', cleaned_body)
        if match:
            code = match.group(0)
            print(f'Strategy 4 (any digits) found: {code}')
            return code
        
        print('No verification code found with any strategy')
        return None
    
    def get_sms_messages(self, limit: int = 50, subject_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch SMS messages with optional filtering
        
        Args:
            limit: Maximum number of messages to fetch
            subject_filter: Filter messages by subject content
            
        Returns:
            List of SMS message objects
        """
        url = f"{self.base_url}/messages?limit={limit}"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            messages = data.get('items', [])
            print(f'Found {len(messages)} total messages')
            
            # Filter by subject if specified
            if subject_filter:
                filtered_messages = []
                for message in messages:
                    if (message.get('Content', {}).get('Headers', {}).get('Subject') and
                        any(subject_filter in subject for subject in message['Content']['Headers']['Subject'])):
                        filtered_messages.append(message)
                messages = filtered_messages
                print(f'Filtered to {len(messages)} messages')
            
            return messages
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch SMS messages: {e}")
    
    def get_latest_verification_code(
        self, 
        phone_number: str, 
        max_attempts: int = 10, 
        retry_delay: int = 3
    ) -> str:
        """
        Fetch the latest verification code from SMS messages for a specific phone number
        
        Args:
            phone_number: Phone number to filter SMS messages by
            max_attempts: Maximum number of retry attempts
            retry_delay: Delay between retry attempts in seconds
            
        Returns:
            The verification code
            
        Raises:
            Exception: If no verification code is found after all attempts
        """
        print(f'Starting SMS verification code retrieval for phone number: {phone_number}')
        print(f'Max attempts: {max_attempts}, Retry delay: {retry_delay}s')
        
        for attempt in range(1, max_attempts + 1):
            print(f'Attempt {attempt}/{max_attempts} - Fetching SMS messages...')
            
            try:
                messages = self.get_sms_messages(limit=50)
                
                # Find the most recent SMS message for the specific phone number
                for message in messages:
                    content = message.get('Content', {})
                    headers = content.get('Headers', {})
                    subjects = headers.get('Subject', [])
                    
                    if subjects:
                        subject = subjects[0]
                        print(f'Checking message subject: {subject}')
                        
                        # Check if this is an SMS for the specific phone number
                        if 'SMS' in subject and phone_number in subject:
                            print(f'Found SMS for phone number: {phone_number}')
                            body = content.get('Body', '')
                            print(f'== Found body: {body}')
                            
                            # Clean and extract verification code
                            cleaned_body = self.clean_sms_body(body)
                            print(f'== Cleaned body: {cleaned_body}')
                            
                            verification_code = self.extract_verification_code(cleaned_body)
                            print(f'== Code match: {verification_code}')
                            
                            if verification_code:
                                print(f'Successfully extracted verification code: {verification_code}')
                                return verification_code
                
                print(f'No SMS found for phone number {phone_number} in attempt {attempt}')
                
                # Wait before next attempt (except on last attempt)
                if attempt < max_attempts:
                    print(f'Waiting {retry_delay}s before next attempt...')
                    time.sleep(retry_delay)
                    
            except Exception as e:
                print(f'Error in attempt {attempt}: {e}')
                if attempt == max_attempts:
                    raise
                
                if attempt < max_attempts:
                    print(f'Waiting {retry_delay}s before retrying after error...')
                    time.sleep(retry_delay)
        
        raise Exception(f'No verification code found for phone number {phone_number} after {max_attempts} attempts')
    
    def get_latest_verification_code_fallback(
        self, 
        max_attempts: int = 10, 
        retry_delay: int = 3
    ) -> str:
        """
        Fallback method to get latest verification code without phone number filtering
        
        Args:
            max_attempts: Maximum number of retry attempts
            retry_delay: Delay between retry attempts in seconds
            
        Returns:
            The verification code
            
        Raises:
            Exception: If no verification code is found after all attempts
        """
        print('Starting SMS verification code retrieval (fallback mode - no phone filtering)')
        print(f'Max attempts: {max_attempts}, Retry delay: {retry_delay}s')
        
        for attempt in range(1, max_attempts + 1):
            print(f'Fallback attempt {attempt}/{max_attempts} - Fetching SMS messages...')
            
            try:
                messages = self.get_sms_messages(limit=50)
                
                # Find the most recent SMS message (without phone filtering)
                for message in messages:
                    content = message.get('Content', {})
                    headers = content.get('Headers', {})
                    subjects = headers.get('Subject', [])
                    
                    if subjects and 'SMS' in subjects[0]:
                        print('Found SMS message (fallback mode)')
                        body = content.get('Body', '')
                        print(f'== Fallback body: {body}')
                        
                        # Clean and extract verification code
                        cleaned_body = self.clean_sms_body(body)
                        print(f'== Fallback cleaned body: {cleaned_body}')
                        
                        verification_code = self.extract_verification_code(cleaned_body)
                        print(f'== Fallback code match: {verification_code}')
                        
                        if verification_code:
                            print(f'Successfully extracted verification code (fallback): {verification_code}')
                            return verification_code
                
                print(f'No SMS found in fallback attempt {attempt}')
                
                # Wait before next attempt (except on last attempt)
                if attempt < max_attempts:
                    print(f'Waiting {retry_delay}s before next fallback attempt...')
                    time.sleep(retry_delay)
                    
            except Exception as e:
                print(f'Error in fallback attempt {attempt}: {e}')
                if attempt == max_attempts:
                    raise
                
                if attempt < max_attempts:
                    print(f'Waiting {retry_delay}s before retrying fallback after error...')
                    time.sleep(retry_delay)
        
        raise Exception(f'No verification code found in any recent SMS messages after {max_attempts} attempts (fallback mode)')


# Convenience functions for direct usage
def get_otp_for_phone(phone_number: str, max_attempts: int = 10, retry_delay: int = 3) -> str:
    """
    Get OTP for specific phone number (convenience function)
    
    Args:
        phone_number: Phone number to get OTP for
        max_attempts: Maximum retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        Verification code
    """
    sms_helper = SMSHelper()
    return sms_helper.get_latest_verification_code(phone_number, max_attempts, retry_delay)


def get_latest_otp(max_attempts: int = 10, retry_delay: int = 3) -> str:
    """
    Get latest OTP without phone filtering (convenience function)
    
    Args:
        max_attempts: Maximum retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        Verification code
    """
    sms_helper = SMSHelper()
    return sms_helper.get_latest_verification_code_fallback(max_attempts, retry_delay)