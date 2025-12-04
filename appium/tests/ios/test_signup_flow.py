"""iOS Signup Flow Test"""

import pytest
from tests.shared.signup_flow_shared import SignUpFlowShared


@pytest.mark.ios
@pytest.mark.signup
class TestiOSSignUpFlow(SignUpFlowShared):
    """iOS-specific signup flow tests"""
    
    @pytest.mark.smoke
    def test_ios_signup_flow_simulator(self):
        """Test complete signup flow on iOS simulator"""
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
    
    @pytest.mark.device
    def test_ios_signup_flow_device(self):
        """Test complete signup flow on iOS real device"""
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
    
    @pytest.mark.regression
    def test_ios_signup_flow_with_custom_data(self):
        """Test signup flow with custom test data on iOS"""
        # Override test data
        self.test_data.update({
            'password': 'CustomPass123@',
            'first_name': 'John',
            'last_name': 'Doe',
            'passcode': '123456'
        })
        
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
        
        # Verify custom data was used
        personal_info = test_results['generated_data']['personal_info']
        assert personal_info['first_name'] == 'John'
        assert personal_info['last_name'] == 'Doe'
        assert personal_info['password'] == 'CustomPass123@'
    
    @pytest.mark.parametrize("passcode", ["000000", "111111", "123456"])
    def test_ios_signup_with_different_passcodes(self, passcode):
        """Test signup flow with different passcodes"""
        self.test_data['passcode'] = passcode
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
        
        # Verify passcode was used
        passcode_info = test_results['generated_data']['passcode_info']
        assert passcode_info['passcode'] == passcode
    
    def test_ios_signup_flow_screenshot_verification(self):
        """Test signup flow with emphasis on screenshot capture"""
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
        
        # Verify screenshots were taken at each major step
        screenshots = test_results['screenshots']
        assert len(screenshots) >= 6, f"Expected at least 6 screenshots, got {len(screenshots)}"
        
        # Print screenshot paths for manual verification
        print("\nScreenshots taken:")
        for screenshot in screenshots:
            print(f"  - {screenshot}")


# Fixtures for iOS-specific test configuration
@pytest.fixture(scope="class", autouse=True)
def ios_test_setup(request):
    """Setup for iOS tests"""
    print("\nSetting up iOS test environment...")
    
    # You can add iOS-specific setup here
    # For example: checking iOS simulator availability, app installation, etc.
    
    yield
    
    print("\nTearing down iOS test environment...")
    # iOS-specific cleanup


# Custom markers for iOS tests
pytestmark = [
    pytest.mark.ios,
    pytest.mark.signup
]