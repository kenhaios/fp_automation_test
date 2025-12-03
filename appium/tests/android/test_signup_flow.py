"""Android Signup Flow Test"""

import pytest
from tests.shared.signup_flow_shared import SignUpFlowShared


@pytest.mark.android
@pytest.mark.signup
class TestAndroidSignUpFlow(SignUpFlowShared):
    """Android-specific signup flow tests"""
    
    @pytest.mark.smoke
    def test_android_signup_flow_emulator(self):
        """Test complete signup flow on Android emulator"""
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
    
    @pytest.mark.device
    @pytest.mark.skip(reason="Requires real Android device connected via ADB")
    def test_android_signup_flow_device(self):
        """Test complete signup flow on Android real device"""
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
    
    @pytest.mark.regression
    def test_android_signup_flow_with_custom_data(self):
        """Test signup flow with custom test data on Android"""
        # Override test data
        self.test_data.update({
            'password': 'AndroidTest123@',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'passcode': '654321'
        })
        
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
        
        # Verify custom data was used
        personal_info = test_results['generated_data']['personal_info']
        assert personal_info['first_name'] == 'Jane'
        assert personal_info['last_name'] == 'Smith'
        assert personal_info['password'] == 'AndroidTest123@'
    
    @pytest.mark.parametrize("device_orientation", ["portrait", "landscape"])
    @pytest.mark.skip(reason="Orientation testing requires device rotation implementation")
    def test_android_signup_different_orientations(self, device_orientation):
        """Test signup flow in different device orientations"""
        # Rotate device to specified orientation
        if device_orientation == "landscape":
            self.driver.orientation = "LANDSCAPE"
        else:
            self.driver.orientation = "PORTRAIT"
        
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
    
    def test_android_signup_flow_with_back_navigation(self):
        """Test signup flow with Android back button navigation"""
        from src.pages.welcome_page import WelcomePage
        from src.pages.signup_page import SignUpPage
        
        # Start signup flow
        welcome_page = WelcomePage(self.driver)
        welcome_page.navigate_to_signup()
        
        # Navigate to signup page and then use back button
        signup_page = SignUpPage(self.driver)
        
        # Press Android back button
        self.driver.back()
        
        # Should return to welcome screen
        assert welcome_page.is_welcome_message_visible(), "Back navigation failed"
        
        # Continue with normal flow
        welcome_page.navigate_to_signup()
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
    
    def test_android_signup_flow_keyboard_handling(self):
        """Test signup flow with Android keyboard interactions"""
        from src.pages.welcome_page import WelcomePage
        from src.pages.signup_page import SignUpPage
        from src.utils.phone_generator import PhoneGenerator
        
        welcome_page = WelcomePage(self.driver)
        welcome_page.navigate_to_signup()
        
        signup_page = SignUpPage(self.driver)
        signup_page.select_personal_account()
        
        # Test keyboard appears and can be hidden
        phone_number = PhoneGenerator.generate_random_phone()
        signup_page.enter_phone_number(phone_number)
        
        # Hide keyboard using Android method
        signup_page.hide_keyboard()
        
        # Continue with normal flow
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
    
    def test_android_signup_permissions_handling(self):
        """Test signup flow with Android permissions handling"""
        # Note: This test assumes the app might request permissions during signup
        # In practice, you would handle permission dialogs here
        
        test_results = self.execute_signup_flow()
        self.verify_test_results(test_results)
        
        # Verify no permission-related errors occurred
        assert not any("permission" in error.lower() for error in test_results['errors'])


# Fixtures for Android-specific test configuration
@pytest.fixture(scope="class", autouse=True)
def android_test_setup(request):
    """Setup for Android tests"""
    print("\nSetting up Android test environment...")
    
    # You can add Android-specific setup here
    # For example: checking emulator status, app installation, adb connection, etc.
    
    yield
    
    print("\nTearing down Android test environment...")
    # Android-specific cleanup


@pytest.fixture
def android_device_info(request):
    """Get Android device information for tests"""
    if hasattr(request.instance, 'driver') and request.instance.driver:
        device_info = request.instance.get_device_info()
        print(f"\nAndroid device info: {device_info}")
        return device_info
    return {}


# Custom markers for Android tests
pytestmark = [
    pytest.mark.android,
    pytest.mark.signup
]