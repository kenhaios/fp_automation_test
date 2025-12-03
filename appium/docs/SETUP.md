# FasterPay E-Wallet Appium Test Setup Guide

This guide provides comprehensive instructions for setting up and running Appium tests for the FasterPay E-Wallet mobile application.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Setup](#quick-setup)
- [Manual Setup](#manual-setup)
- [Running Tests](#running-tests)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **Operating System**: macOS (for iOS testing), Linux, or Windows
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm**: 8.0 or higher

### Platform-Specific Requirements

#### iOS Testing (macOS only)
- **Xcode**: Latest version with Command Line Tools
- **iOS Simulator**: Available simulators for testing
- **Real Device**: iOS device with Developer Mode enabled (optional)

#### Android Testing (All platforms)
- **Android SDK**: Android Studio or standalone SDK
- **Java JDK**: 8 or higher
- **Android Emulator**: At least one AVD configured
- **Real Device**: Android device with USB debugging enabled (optional)

## Quick Setup

### 1. Clone and Navigate
```bash
cd fp_automation_test/appium
```

### 2. Run Setup Script
```bash
# Install all dependencies
python setup/install_dependencies.py

# iOS-specific setup (macOS only)
python setup/setup_ios.py

# Android-specific setup
python setup/setup_android.py
```

### 3. Activate Virtual Environment (if created)
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Place App Files
- Place iOS app file in `apps/ios/FasterpayEwallet.app`
- Place Android APK in `apps/android/fasterpay-ewallet.apk`

### 5. Start Appium and Run Tests
```bash
# Start Appium server (in separate terminal)
appium

# Run tests
pytest tests/ios/ --platform=ios_simulator
pytest tests/android/ --platform=android_emulator
```

## Manual Setup

### 1. Install Python Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Install Appium Server
```bash
# Install Appium globally
npm install -g appium

# Install Appium Doctor
npm install -g @appium/doctor

# Install drivers
appium driver install xcuitest      # iOS
appium driver install uiautomator2  # Android
```

### 3. Platform Setup

#### iOS Setup (macOS)
```bash
# Install iOS development tools
xcode-select --install

# Install device support tools
brew install libimobiledevice
brew install ideviceinstaller
brew install ios-webkit-debug-proxy

# Verify setup
appium-doctor --ios
```

#### Android Setup
```bash
# Set environment variables
export ANDROID_HOME=/path/to/android-sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Install platform tools (macOS)
brew install android-platform-tools

# Verify setup
appium-doctor --android
```

### 4. Verify Installation
```bash
# Check Appium installation
appium --version

# Check drivers
appium driver list

# Run Appium Doctor
appium-doctor
```

## Running Tests

### Test Execution Commands

#### iOS Tests
```bash
# iOS Simulator
pytest tests/ios/ --platform=ios_simulator

# iOS Real Device (requires UDID)
pytest tests/ios/ --platform=ios_device --device-id=YOUR_DEVICE_UDID

# Specific test with markers
pytest tests/ios/ -m smoke --platform=ios_simulator
```

#### Android Tests
```bash
# Android Emulator
pytest tests/android/ --platform=android_emulator

# Android Real Device (requires device ID)
pytest tests/android/ --platform=android_device --device-id=YOUR_DEVICE_ID

# Specific test with markers
pytest tests/android/ -m smoke --platform=android_emulator
```

#### Cross-Platform Tests
```bash
# Run all signup tests
pytest tests/ -m signup

# Run smoke tests on both platforms
pytest tests/ -m smoke

# Parallel execution
pytest tests/ -n 2 --platform=ios_simulator
```

### Test Markers
- `ios`: iOS platform tests
- `android`: Android platform tests
- `simulator`: Simulator/emulator tests
- `device`: Real device tests
- `smoke`: Smoke tests
- `regression`: Regression tests
- `signup`: Sign up flow tests

### Test Reports
```bash
# HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Allure report
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Configuration

### Device Configuration

#### iOS Simulator Configuration
Edit `config/ios_simulator.py`:
```python
SIMULATOR_DEVICES = {
    "iphone_14": {"device_name": "iPhone 14", "ios_version": "16.0"},
    "iphone_13": {"device_name": "iPhone 13", "ios_version": "15.0"}
}
```

#### iOS Real Device Configuration
Edit `config/ios_device.py`:
```python
# Update with your Apple Developer Team ID
"appium:xcodeOrgId": "YOUR_TEAM_ID",
"appium:xcodeSigningId": "iPhone Developer"
```

#### Android Emulator Configuration
Edit `config/android_simulator.py`:
```python
EMULATOR_DEVICES = {
    "pixel_4_api_30": {"avd_name": "Pixel_4_API_30", "android_version": "11"},
    "pixel_6_api_33": {"avd_name": "Pixel_6_API_33", "android_version": "13"}
}
```

### Environment Variables
```bash
# Appium server URL (default: http://localhost:4723)
export APPIUM_SERVER_URL=http://localhost:4723

# Android SDK path
export ANDROID_HOME=/path/to/android-sdk

# iOS Team ID for real device testing
export IOS_TEAM_ID=YOUR_TEAM_ID
```

### Test Data Configuration
Tests use configurable test data in `tests/shared/signup_flow_shared.py`:
```python
self.test_data = {
    'password': '12345Aa@',
    'first_name': 'Hellen',
    'last_name': 'Johnson',
    'passcode': '000000'
}
```

## Project Structure
```
appium/
├── config/                    # Device configurations
├── src/
│   ├── base/                 # Base classes
│   ├── pages/                # Page Object Model
│   ├── utils/                # Utility functions
├── tests/
│   ├── ios/                  # iOS tests
│   ├── android/              # Android tests
│   └── shared/               # Shared test logic
├── apps/                     # App binaries
├── reports/                  # Test reports
├── screenshots/              # Test screenshots
├── setup/                    # Setup scripts
└── docs/                     # Documentation
```

## Environment Management

### Virtual Environment
```bash
# Create
python3 -m venv venv

# Activate
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# Deactivate
deactivate
```

### Dependency Management
```bash
# Install dependencies
pip install -r requirements.txt

# Update requirements
pip freeze > requirements.txt

# Install development dependencies
pip install -r requirements.txt[dev]
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Appium Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: npm install -g appium
      - run: appium driver install xcuitest
      - run: pip install -r requirements.txt
      - run: appium &
      - run: pytest tests/ios/ -m smoke
```

## Next Steps

1. **Place App Files**: Copy your iOS and Android app files to the appropriate directories
2. **Configure Devices**: Update device configurations with your specific requirements
3. **Run Sample Test**: Execute a simple test to verify setup
4. **Customize Tests**: Modify test data and add additional test cases
5. **Setup CI/CD**: Integrate with your continuous integration pipeline

For detailed device setup instructions, see [DEVICE_SETUP.md](DEVICE_SETUP.md).
For troubleshooting common issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).