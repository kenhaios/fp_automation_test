# Appium Inspector Setup Guide

## Quick Fix for "Invalid or unsupported WebDriver capabilities" Error

If you're getting the capability error when connecting Appium Inspector, use one of the pre-configured capability files below.

### Step-by-Step Instructions:

1. **Start Appium Server**
   ```bash
   cd /Users/kenha/Documents/2_Automation/FP_AutomationTest/fp_automation_test/appium
   appium --port 4723
   ```

2. **Open Appium Inspector**
   - Set Remote Host: `localhost`
   - Set Remote Port: `4723`
   - Set Remote Path: `/`

3. **Choose the Right Capability Configuration**

   Copy capabilities from one of these files based on your setup:

   **For iOS Simulator (W3C Format):**
   ```json
   {
     "platformName": "iOS",
     "appium:platformVersion": "17.2",
     "appium:deviceName": "iPhone 14",
     "appium:automationName": "XCUITest",
     "appium:app": "/Users/kenha/Documents/2_Automation/FP_AutomationTest/fp_automation_test/appium/apps/ios/Fasterpay.app",
     "appium:bundleId": "com.fasterpay.app.staging",
     "appium:noReset": false,
     "appium:newCommandTimeout": 300
   }
   ```

   **For iOS Simulator (Legacy Format):**
   ```json
   {
     "platformName": "iOS",
     "platformVersion": "17.2",
     "deviceName": "iPhone 14",
     "automationName": "XCUITest",
     "app": "/Users/kenha/Documents/2_Automation/FP_AutomationTest/fp_automation_test/appium/apps/ios/Fasterpay.app",
     "bundleId": "com.fasterpay.app.staging",
     "noReset": false,
     "newCommandTimeout": 300
   }
   ```

4. **Click "Start Session"**

## Available Configuration Files

All configuration files are located in `config/` directory:

### W3C WebDriver Compliant (Recommended):
- `inspector_ios_simulator.json` - For iOS Simulator
- `inspector_ios_device.json` - For Real iOS Device

### Legacy Format (If W3C fails):
- `inspector_ios_simulator_legacy.json` - For iOS Simulator (legacy)
- `inspector_ios_device_legacy.json` - For Real iOS Device (legacy)

## Troubleshooting Common Issues

### 1. "automationName" Error
**Problem:** Inspector doesn't recognize `appium:automationName` capability.

**Solutions:**
1. Try the legacy format files (without `appium:` prefix)
2. Use an older version of Appium Inspector
3. Update to the latest Appium Inspector version

### 2. App Not Found Error
**Problem:** Inspector can't find the app file.

**Solution:** Update the app path in the configuration:
```json
{
  "appium:app": "/full/path/to/your/app/Fasterpay.app"
}
```

### 3. Device Connection Issues
**Problem:** Can't connect to simulator or device.

**Solutions:**
1. **For Simulator:**
   - Make sure iOS Simulator is running
   - Check that the device name matches exactly (case-sensitive)
   - Verify iOS version is correct

2. **For Real Device:**
   - Update UDID in configuration
   - Ensure device is connected and trusted
   - Check developer certificates are valid

### 4. Bundle ID Issues
**Problem:** App won't launch due to bundle ID mismatch.

**Solution:** Verify the correct bundle ID:
```bash
# For .app files (simulator)
/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" /path/to/app/Info.plist

# For .ipa files (device)
unzip -q app.ipa && /usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" Payload/*.app/Info.plist
```

## Utility Script

Use the included utility script to generate fresh configurations:

```bash
cd /Users/kenha/Documents/2_Automation/FP_AutomationTest/fp_automation_test/appium
python utils/inspector_helper.py
```

This will:
- Check available simulators and connected devices
- Generate all necessary configuration files
- Provide usage instructions

## Inspector Version Compatibility

| Appium Inspector Version | Recommended Capability Format |
|-------------------------|-------------------------------|
| 2024.x.x (Latest)      | W3C format (`appium:` prefix) |
| 2023.x.x               | W3C format (`appium:` prefix) |
| 2022.x.x and older     | Legacy format (no prefix)    |

## Quick Commands Reference

```bash
# Check connected devices
xcrun simctl list devices available

# Start specific simulator
xcrun simctl boot "iPhone 14"

# Check real device UDID
xcrun xctrace list devices

# Start Appium server with logging
appium --port 4723 --log-level debug

# Generate new Inspector configs
python utils/inspector_helper.py
```

## Still Having Issues?

1. **Check Appium Server Logs:** Look for specific error messages when Inspector tries to connect
2. **Verify App Installation:** Make sure your app is properly built and accessible
3. **Update Tools:** Ensure you have compatible versions of Appium, Inspector, and Xcode
4. **Try Minimal Capabilities:** Start with just `platformName`, `deviceName`, and `automationName`

If you continue having issues, check the Appium Inspector logs and Appium server logs for more specific error details.