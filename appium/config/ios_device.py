"""iOS Real Device configuration for Appium tests"""

from typing import Dict, Any

def get_ios_device_caps(udid: str, device_name: str = "iPhone", ios_version: str = "16.0") -> Dict[str, Any]:
    """
    Get iOS real device capabilities for Appium
    
    Args:
        udid: Device UDID
        device_name: Name of iOS device
        ios_version: iOS version
        
    Returns:
        Dictionary of Appium capabilities
    """
    return {
        "platformName": "iOS",
        "appium:platformVersion": ios_version,
        "appium:deviceName": device_name,
        "appium:udid": udid,
        "appium:automationName": "XCUITest",
        "appium:app": "apps/ios/Fasterpay.ipa",
        "appium:bundleId": "com.fasterpay.app.staging",
        "appium:noReset": False,
        "appium:fullReset": True,
        "appium:newCommandTimeout": 300,
        "appium:commandTimeouts": {
            "default": 60000
        },
        "appium:waitForQuiescence": False,
        "appium:shouldUseCompactResponses": False,
        "appium:elementResponseAttributes": "type,name,label,enabled,visible,accessible,x,y,width,height",
        # Real device specific settings
        "appium:xcodeOrgId": "37N222R38X",  # Replace with your Apple Developer Team ID
        "appium:xcodeSigningId": "iPhone Developer",
        "appium:usePrebuiltWDA": False,
        "appium:derivedDataPath": "/tmp/derivedData",
        "appium:useNewWDA": True
    }

def get_device_info_from_udid(udid: str) -> Dict[str, str]:
    """
    Get device information from UDID
    Note: In a real implementation, you might query this from device
    
    Args:
        udid: Device UDID
        
    Returns:
        Dictionary with device name and iOS version
    """
    # This is a placeholder - in real implementation you'd query device info
    return {
        "device_name": "iPhone",
        "ios_version": "16.0"
    }