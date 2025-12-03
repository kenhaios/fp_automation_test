"""Shared signup flow logic for both iOS and Android"""

import pytest
from src.base.base_test import BaseTest
from src.pages.welcome_page import WelcomePage
from src.pages.signup_page import SignUpPage
from src.pages.personal_info_page import PersonalInfoPage
from src.pages.address_page import AddressPage
from src.pages.passcode_page import PasscodePage
from src.pages.account_page import AccountPage
from src.utils.phone_generator import PhoneGenerator
from src.utils.sms_helper import SMSHelper
from src.utils.test_helper import TestHelper


class SignUpFlowShared(BaseTest):
    """Shared signup flow test logic"""
    
    def setup_method(self):
        """Setup before each test"""
        self.phone_generator = PhoneGenerator()
        self.sms_helper = SMSHelper()
        self.test_helper = TestHelper()
        
        # Test data
        self.test_data = {
            'password': '12345Aa@',
            'first_name': 'Hellen',
            'last_name': 'Johnson',
            'passcode': '000000'
        }
    
    def execute_signup_flow(self) -> dict:
        """
        Execute the complete signup flow
        
        Returns:
            Dictionary with test results and generated data
        """
        test_results = {
            'success': False,
            'generated_data': {},
            'screenshots': [],
            'errors': []
        }
        
        try:
            # Step 1: Navigate through welcome screen
            TestHelper.log_test_step("Starting signup flow", "Navigating through welcome screen")
            welcome_page = WelcomePage(self.driver)
            welcome_page.navigate_to_signup()
            test_results['screenshots'].append(welcome_page.take_screenshot("welcome_completed"))
            
            # Step 2: Phone number setup and OTP
            TestHelper.log_test_step("Phone verification", "Generating phone and setting up verification")
            signup_page = SignUpPage(self.driver)
            
            # Generate phone number
            phone_number = self.phone_generator.generate_random_phone()
            test_results['generated_data']['phone_number'] = phone_number
            TestHelper.log_test_step("Generated phone number", phone_number)
            
            # Complete phone setup
            entered_phone = signup_page.complete_phone_verification_setup(phone_number)
            test_results['generated_data']['entered_phone'] = entered_phone
            test_results['screenshots'].append(signup_page.take_screenshot("phone_setup_completed"))
            
            # Step 3: Get OTP from SMS
            TestHelper.log_test_step("OTP retrieval", "Fetching verification code from SMS")
            try:
                otp_code = self.sms_helper.get_latest_verification_code(
                    phone_number=phone_number,
                    max_attempts=10,
                    retry_delay=3
                )
                test_results['generated_data']['otp_code'] = otp_code
                TestHelper.log_test_step("OTP retrieved", otp_code)
            except Exception as e:
                TestHelper.log_test_step("OTP retrieval failed, trying fallback")
                otp_code = self.sms_helper.get_latest_verification_code_fallback(
                    max_attempts=5,
                    retry_delay=3
                )
                test_results['generated_data']['otp_code'] = otp_code
                TestHelper.log_test_step("OTP retrieved (fallback)", otp_code)
            
            # Step 4: Complete personal information
            TestHelper.log_test_step("Personal info", "Completing personal information section")
            personal_info_page = PersonalInfoPage(self.driver)
            personal_info = personal_info_page.complete_personal_info(
                otp_code=otp_code,
                email=None,  # Will generate random email
                password=self.test_data['password'],
                first_name=self.test_data['first_name'],
                last_name=self.test_data['last_name']
            )
            test_results['generated_data']['personal_info'] = personal_info
            test_results['screenshots'].append(personal_info_page.take_screenshot("personal_info_completed"))
            
            # Step 5: Complete address information
            TestHelper.log_test_step("Address info", "Completing address information")
            address_page = AddressPage(self.driver)
            address_info = address_page.complete_address_info()
            test_results['generated_data']['address_info'] = address_info
            test_results['screenshots'].append(address_page.take_screenshot("address_completed"))
            
            # Step 6: Complete passcode setup
            TestHelper.log_test_step("Passcode setup", "Setting up account passcode")
            passcode_page = PasscodePage(self.driver)
            passcode_info = passcode_page.complete_passcode_setup(
                passcode=self.test_data['passcode'],
                skip_dob=True
            )
            test_results['generated_data']['passcode_info'] = passcode_info
            test_results['screenshots'].append(passcode_page.take_screenshot("passcode_completed"))
            
            # Step 7: Verify account creation and perform logout
            TestHelper.log_test_step("Account verification", "Verifying account creation and testing logout")
            account_page = AccountPage(self.driver)
            account_page.assert_account_page_loaded()
            test_results['screenshots'].append(account_page.take_screenshot("account_loaded"))
            
            # Test logout flow
            logout_success = account_page.perform_logout_flow()
            test_results['generated_data']['logout_success'] = logout_success
            test_results['screenshots'].append(account_page.take_screenshot("logout_completed"))
            
            if logout_success:
                TestHelper.log_test_step("Signup flow completed", "All steps completed successfully")
                test_results['success'] = True
            else:
                test_results['errors'].append("Logout verification failed")
            
        except Exception as e:
            error_msg = f"Signup flow failed: {str(e)}"
            TestHelper.log_test_step("Error occurred", error_msg)
            test_results['errors'].append(error_msg)
            
            # Take screenshot on failure
            try:
                failure_screenshot = TestHelper.take_screenshot_on_failure(self.driver, "signup_flow_failure")
                test_results['screenshots'].append(failure_screenshot)
            except:
                pass
        
        return test_results
    
    def verify_test_results(self, test_results: dict) -> None:
        """
        Verify and assert test results
        
        Args:
            test_results: Results from signup flow execution
        """
        # Print test summary
        print(f"\n{'='*50}")
        print("SIGNUP FLOW TEST RESULTS")
        print(f"{'='*50}")
        print(f"Success: {test_results['success']}")
        print(f"Screenshots taken: {len(test_results['screenshots'])}")
        print(f"Errors: {len(test_results['errors'])}")
        
        if test_results['generated_data']:
            print(f"\nGenerated Test Data:")
            for key, value in test_results['generated_data'].items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {sub_value}")
                else:
                    print(f"  {key}: {value}")
        
        if test_results['errors']:
            print(f"\nErrors encountered:")
            for error in test_results['errors']:
                print(f"  - {error}")
        
        print(f"{'='*50}\n")
        
        # Assert test success
        assert test_results['success'], f"Signup flow failed: {test_results['errors']}"
        
        # Verify key data was generated
        assert 'phone_number' in test_results['generated_data'], "Phone number was not generated"
        assert 'otp_code' in test_results['generated_data'], "OTP code was not retrieved"
        assert 'personal_info' in test_results['generated_data'], "Personal info was not completed"
        assert 'address_info' in test_results['generated_data'], "Address info was not completed"
        assert 'logout_success' in test_results['generated_data'], "Logout was not tested"
        
        # Verify logout was successful
        assert test_results['generated_data']['logout_success'], "Logout verification failed"