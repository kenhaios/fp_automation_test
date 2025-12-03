"""Android Real Device configuration for Appium tests"""

from typing import Dict, Any

def get_android_device_caps(device_id: str, android_version: str = "11") -> Dict[str, Any]:
    """
    Get Android real device capabilities for Appium
    
    Args:
        device_id: Device ID (from adb devices)
        android_version: Android version
        
    Returns:
        Dictionary of Appium capabilities
    """
    return {
        "platformName": "Android",
        "appium:platformVersion": android_version,
        "appium:deviceName": "Android Device",
        "appium:udid": device_id,
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
        # Real device specific settings
        "appium:autoGrantPermissions": True,
        "appium:disableWindowAnimation": True,
        "appium:skipServerInstallation": False,
        "appium:skipDeviceInitialization": False,
        "appium:ignoreUnimportantViews": False
    }

def get_device_info_from_id(device_id: str) -> Dict[str, str]:
    """
    Get device information from device ID
    Note: In a real implementation, you might query this via ADB
    
    Args:
        device_id: Device ID
        
    Returns:
        Dictionary with device name and Android version
    """
    # This is a placeholder - in real implementation you'd query via ADB
    import subprocess
    try:
        # Get Android version
        version_output = subprocess.check_output(
            f"adb -s {device_id} shell getprop ro.build.version.release",
            shell=True,
            text=True
        ).strip()
        
        # Get device model
        model_output = subprocess.check_output(
            f"adb -s {device_id} shell getprop ro.product.model",
            shell=True,
            text=True
        ).strip()
        
        return {
            "device_name": model_output,
            "android_version": version_output
        }
    except subprocess.CalledProcessError:
        return {
            "device_name": "Android Device",
            "android_version": "11"
        }