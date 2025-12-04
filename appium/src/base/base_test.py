"""Base Test class with setup and teardown functionality"""

import pytest
import os
from typing import Dict, Any
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options

from config.ios_simulator import get_ios_simulator_caps, SIMULATOR_DEVICES
from config.ios_device import get_ios_device_caps
from config.android_simulator import get_android_emulator_caps, EMULATOR_DEVICES
from config.android_device import get_android_device_caps


class BaseTest:
    """Base test class with common setup and teardown"""
    
    driver = None
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, request):
        """Setup and teardown for each test"""
        # Get test configuration from pytest markers or environment
        platform = getattr(request.config.option, 'platform', 'ios_simulator')
        device_id = getattr(request.config.option, 'device_id', None)
        
        # Setup driver
        self.setup_driver(platform, device_id)
        
        yield
        
        # Teardown driver
        self.teardown_driver()
    
    def setup_driver(self, platform: str, device_id: str = None) -> None:
        """Setup Appium driver based on platform"""
        appium_server_url = os.getenv('APPIUM_SERVER_URL', 'http://localhost:4723')
        
        caps = self._get_capabilities(platform, device_id)
        
        if platform.startswith('ios'):
            options = XCUITestOptions().load_capabilities(caps)
            self.driver = webdriver.Remote(appium_server_url, options=options)
        else:  # Android
            options = UiAutomator2Options().load_capabilities(caps)
            self.driver = webdriver.Remote(appium_server_url, options=options)
        
        # Set implicit wait
        self.driver.implicitly_wait(10)
    
    def _get_capabilities(self, platform: str, device_id: str = None) -> Dict[str, Any]:
        """Get device capabilities based on platform"""
        if platform == 'ios_simulator':
            device_config = SIMULATOR_DEVICES.get('iphone_14', SIMULATOR_DEVICES['iphone_14'])
            return get_ios_simulator_caps(
                device_config['device_name'], 
                device_config['ios_version']
            )
        elif platform == 'ios_device':
            if not device_id:
                raise ValueError("Device ID required for iOS real device testing")
            return get_ios_device_caps(device_id)
        elif platform == 'android_emulator':
            device_config = EMULATOR_DEVICES.get('pixel_4_api_30', EMULATOR_DEVICES['pixel_4_api_30'])
            return get_android_emulator_caps(
                device_config['avd_name'],
                device_config['android_version']
            )
        elif platform == 'android_device':
            if not device_id:
                raise ValueError("Device ID required for Android real device testing")
            return get_android_device_caps(device_id)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
    
    def teardown_driver(self) -> None:
        """Teardown Appium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def restart_app(self) -> None:
        """Restart the application"""
        self.driver.terminate_app(self._get_bundle_id())
        self.driver.activate_app(self._get_bundle_id())
    
    def _get_bundle_id(self) -> str:
        """Get app bundle ID based on platform"""
        platform_name = self.driver.capabilities.get('platformName', '').lower()
        if platform_name == 'ios':
            return 'com.fasterpay.app.staging'
        else:  # Android
            return 'com.fasterpay.app.staging'
    
    def reset_app(self) -> None:
        """Reset app to initial state"""
        self.driver.reset()
    
    def background_app(self, duration: int = 5) -> None:
        """Put app in background for specified duration"""
        self.driver.background_app(duration)
    
    def get_device_info(self) -> Dict[str, str]:
        """Get device information"""
        return {
            'platform_name': self.driver.capabilities.get('platformName', ''),
            'platform_version': self.driver.capabilities.get('platformVersion', ''),
            'device_name': self.driver.capabilities.get('deviceName', ''),
            'automation_name': self.driver.capabilities.get('automationName', '')
        }


