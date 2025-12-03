# Device Setup Guide

This guide provides detailed instructions for setting up iOS and Android devices for Appium testing.

## iOS Device Setup

### iOS Simulator Setup

#### Prerequisites
- macOS with Xcode installed
- Xcode Command Line Tools

#### Setup Steps
1. **Install Xcode**
   ```bash
   # Install from App Store or download from developer.apple.com
   xcode-select --install
   ```

2. **List Available Simulators**
   ```bash
   xcrun simctl list devices available
   ```

3. **Create New Simulator (if needed)**
   ```bash
   # Example: Create iPhone 14 with iOS 16.0
   xcrun simctl create "iPhone 14 Test" "iPhone 14" "iOS16.0"
   ```

4. **Boot Simulator**
   ```bash
   xcrun simctl boot "iPhone 14"
   open -a Simulator
   ```

#### Configuration
- Edit `config/ios_simulator.py` to add your preferred simulators
- Simulators are automatically discovered by the setup script

### iOS Real Device Setup

#### Prerequisites
- macOS with Xcode installed
- Apple Developer Account
- iOS device with Developer Mode enabled
- USB cable

#### Setup Steps

1. **Enable Developer Mode on Device**
   - iOS 16+: Settings → Privacy & Security → Developer Mode → Enable
   - iOS 15 and below: Connect to Xcode and enable developer mode

2. **Install libimobiledevice**
   ```bash
   brew install libimobiledevice
   brew install ideviceinstaller
   ```

3. **Connect Device and Trust Computer**
   - Connect device via USB
   - Trust this computer when prompted
   - Verify connection: `idevice_id -l`

4. **Configure WebDriverAgent**
   ```bash
   # Find WebDriverAgent project
   find /usr/local/lib/node_modules/appium -name "WebDriverAgent.xcodeproj"
   ```
   
   Open WebDriverAgent.xcodeproj in Xcode:
   - Select WebDriverAgentLib target
   - Set your Development Team
   - Change Bundle Identifier to unique value
   - Repeat for WebDriverAgentRunner target
   - Build project (Cmd+B)

5. **Update Configuration**
   Edit `config/ios_device.py`:
   ```python
   "appium:xcodeOrgId": "YOUR_TEAM_ID",
   "appium:xcodeSigningId": "iPhone Developer"
   ```

6. **Get Device Information**
   ```bash
   # Get device UDID
   idevice_id -l
   
   # Get device name
   ideviceinfo -k DeviceName
   
   # Get iOS version
   ideviceinfo -k ProductVersion
   ```

#### Running Tests on iOS Device
```bash
pytest tests/ios/ --platform=ios_device --device-id=YOUR_DEVICE_UDID
```

## Android Device Setup

### Android Emulator Setup

#### Prerequisites
- Android Studio or Android SDK
- Java JDK 8+
- Android Emulator

#### Setup Steps

1. **Install Android Studio**
   - Download from developer.android.com
   - Install Android SDK and emulator

2. **Set Environment Variables**
   ```bash
   # Add to ~/.bashrc, ~/.zshrc, or equivalent
   export ANDROID_HOME=/path/to/android-sdk
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/emulator
   ```

3. **Create AVD (Android Virtual Device)**
   ```bash
   # List available system images
   avdmanager list targets
   
   # Create AVD
   avdmanager create avd -n Pixel_4_API_30 -k "system-images;android-30;google_apis;x86_64"
   ```

4. **Start Emulator**
   ```bash
   # List available AVDs
   emulator -list-avds
   
   # Start emulator
   emulator -avd Pixel_4_API_30
   ```

5. **Verify Emulator**
   ```bash
   adb devices
   ```

#### Configuration
Edit `config/android_simulator.py` to add your AVDs:
```python
EMULATOR_DEVICES = {
    "pixel_4_api_30": {"avd_name": "Pixel_4_API_30", "android_version": "11"}
}
```

### Android Real Device Setup

#### Prerequisites
- Android device with USB debugging enabled
- USB cable
- ADB (Android Debug Bridge)

#### Setup Steps

1. **Enable Developer Options**
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   - Return to Settings → Developer Options

2. **Enable USB Debugging**
   - In Developer Options, enable:
     - USB Debugging
     - Stay awake
     - Allow mock locations (if needed)

3. **Connect Device**
   ```bash
   # Connect via USB and verify
   adb devices
   
   # Should show device with "device" status
   ```

4. **Trust Computer**
   - When prompted on device, allow USB debugging
   - Check "Always allow from this computer"

5. **Get Device Information**
   ```bash
   # Get device ID
   adb devices
   
   # Get device model
   adb shell getprop ro.product.model
   
   # Get Android version
   adb shell getprop ro.build.version.release
   ```

6. **Install App (if needed)**
   ```bash
   adb install apps/android/fasterpay-ewallet.apk
   ```

#### Running Tests on Android Device
```bash
pytest tests/android/ --platform=android_device --device-id=YOUR_DEVICE_ID
```

## Device Management

### Multiple Devices

#### iOS Multiple Devices
```bash
# List all connected iOS devices
idevice_id -l

# Run tests on specific device
pytest tests/ios/ --platform=ios_device --device-id=DEVICE_1_UDID
pytest tests/ios/ --platform=ios_device --device-id=DEVICE_2_UDID
```

#### Android Multiple Devices
```bash
# List all connected Android devices
adb devices

# Run tests on specific device
pytest tests/android/ --platform=android_device --device-id=device1
pytest tests/android/ --platform=android_device --device-id=device2
```

### Parallel Testing
```bash
# Run tests in parallel on multiple simulators
pytest tests/ios/ -n 2 --platform=ios_simulator

# Run tests in parallel on multiple emulators
pytest tests/android/ -n 2 --platform=android_emulator
```

## Device Troubleshooting

### iOS Issues

#### Device Not Detected
```bash
# Check if device is connected
idevice_id -l

# Reset device connection
sudo killall -9 com.apple.CoreSimulator.CoreSimulatorService
sudo killall -9 SimulatorTrampoline
```

#### WebDriverAgent Issues
- Ensure bundle identifier is unique
- Check Team ID is correct
- Try rebuilding WebDriverAgent in Xcode
- Check device trust settings

#### Simulator Issues
```bash
# Reset all simulators
xcrun simctl erase all

# Boot specific simulator
xcrun simctl boot "iPhone 14"
```

### Android Issues

#### Device Not Detected
```bash
# Restart ADB server
adb kill-server
adb start-server

# Check device authorization
adb devices
```

#### Emulator Issues
```bash
# Cold boot emulator
emulator -avd YOUR_AVD -wipe-data

# Check emulator status
emulator -list-avds
```

#### Permission Issues
- Ensure USB debugging is enabled
- Check computer is trusted
- Try different USB cable/port

### General Appium Issues

#### Driver Issues
```bash
# Reinstall drivers
appium driver uninstall xcuitest
appium driver install xcuitest

appium driver uninstall uiautomator2
appium driver install uiautomator2
```

#### Port Conflicts
```bash
# Check if port 4723 is in use
lsof -i :4723

# Kill Appium process if needed
pkill -f appium
```

## Device Configuration Examples

### iOS Device Configuration
```python
# config/ios_device.py
def get_ios_device_caps(udid: str) -> Dict[str, Any]:
    return {
        "platformName": "iOS",
        "appium:deviceName": "iPhone",
        "appium:udid": udid,
        "appium:automationName": "XCUITest",
        "appium:app": "apps/ios/FasterpayEwallet.app",
        "appium:bundleId": "com.fasterpay.ewallet",
        "appium:xcodeOrgId": "YOUR_TEAM_ID",
        "appium:xcodeSigningId": "iPhone Developer",
        "appium:noReset": False,
        "appium:fullReset": True
    }
```

### Android Device Configuration
```python
# config/android_device.py
def get_android_device_caps(device_id: str) -> Dict[str, Any]:
    return {
        "platformName": "Android",
        "appium:deviceName": "Android Device",
        "appium:udid": device_id,
        "appium:automationName": "UiAutomator2",
        "appium:app": "apps/android/fasterpay-ewallet.apk",
        "appium:appPackage": "com.fasterpay.ewallet",
        "appium:appActivity": "com.fasterpay.ewallet.MainActivity",
        "appium:noReset": False,
        "appium:fullReset": True
    }
```

## Device Verification

### Verification Commands
```bash
# Verify iOS setup
appium-doctor --ios

# Verify Android setup
appium-doctor --android

# Test device connections
python setup/setup_ios.py
python setup/setup_android.py
```

### Health Checks
```bash
# Check all connected devices
python -c "
from src.utils.device_helper import DeviceHelper
print('iOS devices:', DeviceHelper.get_connected_ios_devices())
print('Android devices:', DeviceHelper.get_connected_android_devices())
"
```

For more troubleshooting information, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).