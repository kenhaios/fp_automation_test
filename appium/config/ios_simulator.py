"""iOS Simulator configuration for Appium tests"""

from typing import Dict, Any

def get_ios_simulator_caps(device_name: str = "iPhone 14", ios_version: str = "17.2") -> Dict[str, Any]:
    """
    Get iOS simulator capabilities for Appium
    
    Args:
        device_name: Name of iOS simulator device
        ios_version: iOS version for simulator
        
    Returns:
        Dictionary of Appium capabilities
    """
    return {
        "platformName": "iOS",
        "appium:platformVersion": ios_version,
        "appium:deviceName": device_name,
        "appium:automationName": "XCUITest",
        "appium:app": "apps/ios/Fasterpay.app",
        "appium:bundleId": "com.fasterpay.app.staging",
        "appium:noReset": False,
        "appium:fullReset": True,
        "appium:newCommandTimeout": 300,
        "appium:commandTimeouts": {
            "default": 60000
        },
        "appium:waitForQuiescence": False,
        "appium:shouldUseCompactResponses": False,
        "appium:elementResponseAttributes": "type,name,label,enabled,visible,accessible,x,y,width,height"
    }

# Common simulator devices
SIMULATOR_DEVICES = {
    "iphone_14": {"device_name": "iPhone 14", "ios_version": "17.2"},
    "iphone_14_plus": {"device_name": "iPhone 14 Plus", "ios_version": "17.2"},
    "iphone_15": {"device_name": "iPhone 15", "ios_version": "17.2"},
    "iphone_15_pro": {"device_name": "iPhone 15 Pro", "ios_version": "17.2"},
    "ipad_air": {"device_name": "iPad Air (5th generation)", "ios_version": "17.2"}
}