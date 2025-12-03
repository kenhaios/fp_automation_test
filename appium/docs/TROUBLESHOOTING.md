# Troubleshooting Guide

This guide helps resolve common issues when setting up and running Appium tests.

## Common Setup Issues

### Python Environment Issues

#### Issue: Python Version Compatibility
```
Error: Python 3.8+ is required
```
**Solution:**
```bash
# Check Python version
python3 --version

# Install Python 3.8+ if needed
# macOS: brew install python@3.9
# Ubuntu: sudo apt install python3.9
# Windows: Download from python.org
```

#### Issue: Virtual Environment Problems
```
Error: No module named 'appium'
```
**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Node.js and Appium Issues

#### Issue: Appium Installation Failed
```
Error: npm install -g appium failed
```
**Solution:**
```bash
# Update npm
npm install -g npm@latest

# Clear npm cache
npm cache clean --force

# Try installing with different permissions
sudo npm install -g appium
```

#### Issue: Appium Server Won't Start
```
Error: Appium server failed to start
```
**Solution:**
```bash
# Kill existing Appium processes
pkill -f appium

# Check port availability
lsof -i :4723

# Start Appium with specific address
appium --address 127.0.0.1 --port 4723
```

#### Issue: Appium Driver Installation Failed
```
Error: Could not install driver 'xcuitest'
```
**Solution:**
```bash
# Update Appium
npm install -g appium@latest

# List available drivers
appium driver list

# Install drivers individually
appium driver install xcuitest
appium driver install uiautomator2

# Check installed drivers
appium driver list --installed
```

## iOS-Specific Issues

### iOS Simulator Issues

#### Issue: No iOS Simulators Found
```
Error: No iOS simulators available
```
**Solution:**
```bash
# Check Xcode installation
xcode-select --print-path

# Install Xcode Command Line Tools
xcode-select --install

# List available simulators
xcrun simctl list devices available

# Create new simulator if needed
xcrun simctl create "Test iPhone" "iPhone 14" "iOS16.0"
```

#### Issue: Simulator Won't Boot
```
Error: Failed to boot simulator
```
**Solution:**
```bash
# Reset simulator
xcrun simctl erase all

# Shutdown all simulators
xcrun simctl shutdown all

# Boot specific simulator
xcrun simctl boot "iPhone 14"

# Open Simulator app
open -a Simulator
```

### iOS Real Device Issues

#### Issue: Device Not Detected
```
Error: No iOS devices found
```
**Solution:**
```bash
# Install libimobiledevice
brew install libimobiledevice

# Check device connection
idevice_id -l

# Trust computer on device
# Go to device Settings → General → Device Management
```

#### Issue: WebDriverAgent Build Failed
```
Error: WebDriverAgent build failed
```
**Solution:**
1. Open WebDriverAgent.xcodeproj in Xcode
2. Select WebDriverAgentLib target
3. In Signing & Capabilities:
   - Select your Development Team
   - Change Bundle Identifier to unique value
4. Repeat for WebDriverAgentRunner target
5. Clean and rebuild project

#### Issue: Code Signing Error
```
Error: Code signing failed
```
**Solution:**
```bash
# Check Team ID
security find-identity -v -p codesigning

# Update config with correct Team ID
# Edit config/ios_device.py:
"appium:xcodeOrgId": "YOUR_TEAM_ID"
```

## Android-Specific Issues

### Android SDK Issues

#### Issue: ANDROID_HOME Not Set
```
Error: ANDROID_HOME environment variable not set
```
**Solution:**
```bash
# Find Android SDK path
# Usually: /Users/username/Library/Android/sdk (macOS)
#          /home/username/Android/Sdk (Linux)
#          C:\Users\username\AppData\Local\Android\Sdk (Windows)

# Set environment variables
export ANDROID_HOME=/path/to/android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools

# Add to shell profile (.bashrc, .zshrc)
echo 'export ANDROID_HOME=/path/to/android/sdk' >> ~/.zshrc
```

#### Issue: ADB Not Found
```
Error: adb: command not found
```
**Solution:**
```bash
# Install platform tools
# macOS:
brew install android-platform-tools

# Or add to PATH manually
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Verify ADB
adb version
```

### Android Emulator Issues

#### Issue: No Emulators Available
```
Error: No Android Virtual Devices found
```
**Solution:**
```bash
# List available AVDs
avdmanager list avd

# Create new AVD
avdmanager create avd -n Test_Pixel -k "system-images;android-30;google_apis;x86_64"

# Or use Android Studio AVD Manager
```

#### Issue: Emulator Won't Start
```
Error: Emulator failed to start
```
**Solution:**
```bash
# Check available AVDs
emulator -list-avds

# Start with specific parameters
emulator -avd YOUR_AVD -no-snapshot-load

# Cold boot emulator
emulator -avd YOUR_AVD -wipe-data

# Check system requirements (virtualization enabled)
```

### Android Real Device Issues

#### Issue: Device Not Authorized
```
Error: device unauthorized
```
**Solution:**
1. Enable Developer Options on device:
   - Settings → About Phone → Tap Build Number 7 times
2. Enable USB Debugging:
   - Settings → Developer Options → USB Debugging
3. Connect device and accept authorization prompt
4. Trust this computer permanently

#### Issue: App Installation Failed
```
Error: Installation failed
```
**Solution:**
```bash
# Check device connection
adb devices

# Manually install app
adb install -r apps/android/fasterpay-ewallet.apk

# Check device storage and permissions
adb shell pm list packages | grep fasterpay
```

## Test Execution Issues

### Test Framework Issues

#### Issue: Tests Not Found
```
Error: No tests ran
```
**Solution:**
```bash
# Check test discovery
pytest --collect-only tests/

# Run with verbose output
pytest -v tests/

# Check file naming (must start with test_)
# Check class naming (must start with Test)
```

#### Issue: Import Errors
```
Error: ModuleNotFoundError: No module named 'src'
```
**Solution:**
```bash
# Install project in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Verify package structure has __init__.py files
```

### Appium Connection Issues

#### Issue: Connection Refused
```
Error: Connection refused to Appium server
```
**Solution:**
```bash
# Check if Appium server is running
curl http://localhost:4723/status

# Start Appium server
appium

# Check Appium logs for errors
appium --log-level debug
```

#### Issue: Session Creation Failed
```
Error: Could not create session
```
**Solution:**
```bash
# Check device capabilities
# Verify app path exists
ls -la apps/ios/FasterpayEwallet.app
ls -la apps/android/fasterpay-ewallet.apk

# Check device is connected
idevice_id -l  # iOS
adb devices    # Android

# Run Appium doctor
appium-doctor --ios
appium-doctor --android
```

### Element Location Issues

#### Issue: Element Not Found
```
Error: no such element
```
**Solution:**
1. Use Appium Inspector to verify element locators
2. Add explicit waits:
   ```python
   WebDriverWait(driver, 10).until(
       EC.presence_of_element_located(locator)
   )
   ```
3. Update locators in page objects
4. Check for platform-specific differences

#### Issue: Element Not Clickable
```
Error: element not interactable
```
**Solution:**
```python
# Wait for element to be clickable
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(locator)
)

# Scroll to element if needed
driver.execute_script("arguments[0].scrollIntoView();", element)

# Use tap instead of click for mobile
driver.tap([(x, y)])
```

### SMS/OTP Issues

#### Issue: OTP Not Retrieved
```
Error: No verification code found
```
**Solution:**
1. Check SMS service availability:
   ```bash
   curl http://mail.bamboo.stuffio.com/api/v2/messages?limit=5
   ```
2. Increase retry attempts in SMS helper
3. Use fallback method without phone filtering
4. Verify phone number format

#### Issue: SMS Service Timeout
```
Error: Request timeout
```
**Solution:**
```python
# Increase timeout in SMS helper
sms_helper = SMSHelper()
otp = sms_helper.get_latest_verification_code(
    phone_number=phone,
    max_attempts=15,  # Increase attempts
    retry_delay=5     # Increase delay
)
```

## Performance Issues

### Slow Test Execution

#### Issue: Tests Running Slowly
**Solutions:**
1. Reduce implicit wait times
2. Use explicit waits instead of sleep
3. Disable animations:
   ```python
   # Android
   "appium:disableWindowAnimation": True
   
   # iOS
   "appium:waitForQuiescence": False
   ```
4. Use faster locator strategies (ID > XPath)

### Memory Issues

#### Issue: Out of Memory Errors
**Solutions:**
1. Reset app between tests:
   ```python
   driver.reset()
   ```
2. Use smaller device resolutions
3. Limit parallel test execution
4. Clear app data regularly

## Debugging Tips

### Enable Debug Logging
```bash
# Appium server logs
appium --log-level debug

# Python test logs
pytest -s -v --log-cli-level=DEBUG tests/
```

### Use Appium Inspector
1. Download Appium Inspector
2. Connect to running Appium server
3. Inspect element locators and properties

### Take Screenshots on Failure
```python
# Automatic screenshots are taken in test helper
# Manual screenshot
driver.save_screenshot("debug_screenshot.png")
```

### Video Recording (Android)
```bash
# Start recording
adb shell screenrecord /sdcard/test_recording.mp4

# Stop recording (Ctrl+C)
# Pull recording
adb pull /sdcard/test_recording.mp4
```

## Getting Help

### Check Logs
1. Appium server logs
2. Test execution logs
3. Device logs (iOS Console, Android logcat)

### Useful Commands
```bash
# iOS device logs
idevicesyslog

# Android device logs
adb logcat

# Appium doctor
appium-doctor

# Device information
python -c "
from src.utils.device_helper import DeviceHelper
print(DeviceHelper.check_prerequisites())
"
```

### Community Resources
- [Appium Documentation](http://appium.io/docs/)
- [Appium GitHub Issues](https://github.com/appium/appium/issues)
- [Appium Community Forum](https://discuss.appium.io/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/appium)

### Contact Support
For project-specific issues:
1. Check this troubleshooting guide
2. Review setup documentation
3. Check GitHub issues in project repository
4. Contact development team with:
   - Error messages
   - Log files
   - Environment details
   - Steps to reproduce