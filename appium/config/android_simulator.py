"""Android Emulator configuration for Appium tests"""

from typing import Dict, Any

def get_android_emulator_caps(avd_name: str = "Pixel_4_API_30", android_version: str = "11") -> Dict[str, Any]:
    """
    Get Android emulator capabilities for Appium
    
    Args:
        avd_name: Android Virtual Device name
        android_version: Android version
        
    Returns:
        Dictionary of Appium capabilities
    """
    return {
        "platformName": "Android",
        "appium:platformVersion": android_version,
        "appium:deviceName": avd_name,
        "appium:avd": avd_name,
        "appium:automationName": "UiAutomator2",
        "appium:app": "apps/android/fasterpay-ewallet.apk",
        "appium:appPackage": "com.fasterpay.ewallet",
        "appium:appActivity": "com.fasterpay.ewallet.MainActivity",
        "appium:noReset": False,
        "appium:fullReset": True,
        "appium:newCommandTimeout": 300,
        "appium:uiautomator2ServerInstallTimeout": 60000,
        "appium:uiautomator2ServerLaunchTimeout": 60000,
        "appium:androidInstallTimeout": 120000,
        "appium:adbExecTimeout": 60000,
        # Emulator specific settings
        "appium:avdLaunchTimeout": 120000,
        "appium:avdReadyTimeout": 120000,
        "appium:autoGrantPermissions": True,
        "appium:disableWindowAnimation": True
    }

# Common emulator configurations
EMULATOR_DEVICES = {
    "pixel_4_api_30": {"avd_name": "Pixel_4_API_30", "android_version": "11"},
    "pixel_6_api_33": {"avd_name": "Pixel_6_API_33", "android_version": "13"},
    "nexus_5x_api_29": {"avd_name": "Nexus_5X_API_29", "android_version": "10"},
    "tablet_api_30": {"avd_name": "Pixel_C_API_30", "android_version": "11"}
}