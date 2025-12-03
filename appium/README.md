# FasterPay E-Wallet Appium Test Suite

Comprehensive mobile test automation suite for the FasterPay E-Wallet application using Appium and Python. This project provides cross-platform testing capabilities for both iOS and Android devices/simulators.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- iOS: macOS with Xcode (for iOS testing)
- Android: Android SDK with emulator/device

### Installation
```bash
# Clone and navigate to project
cd fp_automation_test/appium

# Run automated setup
python setup/install_dependencies.py
python setup/setup_ios.py      # macOS only
python setup/setup_android.py

# Activate virtual environment (if created)
source venv/bin/activate

# Start Appium server
appium

# Run tests
pytest tests/ios/ --platform=ios_simulator
pytest tests/android/ --platform=android_emulator
```

## 📱 Supported Platforms

### iOS
- **Simulators**: iPhone/iPad simulators (iOS 15+)
- **Real Devices**: iOS devices with Developer Mode
- **Requirements**: macOS, Xcode, libimobiledevice

### Android
- **Emulators**: Android Virtual Devices (API 29+)
- **Real Devices**: Android devices with USB debugging
- **Requirements**: Android SDK, ADB

## ✨ Features

- **Cross-Platform**: Single test codebase for iOS and Android
- **Page Object Model**: Maintainable and scalable test architecture
- **Utilities**: Phone generation, SMS verification, device management
- **Reporting**: HTML reports, screenshots, Allure integration
- **CI/CD Ready**: GitHub Actions compatible
- **Real Device Support**: Test on physical devices
- **Parallel Execution**: Run tests concurrently

## 🏗️ Architecture

```
appium/
├── config/           # Device configurations
├── src/
│   ├── base/        # Base page and test classes
│   ├── pages/       # Page Object Model
│   └── utils/       # Utility functions
├── tests/
│   ├── ios/         # iOS-specific tests
│   ├── android/     # Android-specific tests
│   └── shared/      # Shared test logic
├── apps/            # Application binaries
├── setup/           # Setup scripts
└── docs/            # Documentation
```

## 🧪 Test Coverage

The test suite currently covers the complete signup flow:

1. **Welcome Screen** - App launch and navigation
2. **Sign Up Flow** - Account type selection and phone input
3. **Phone Verification** - OTP generation and validation
4. **Personal Information** - Email, password, and name input
5. **Address Information** - Address details and location
6. **Passcode Setup** - Security passcode configuration
7. **Account Verification** - Final account validation and logout

## 📖 Documentation

- **[Setup Guide](docs/SETUP.md)** - Complete installation and configuration
- **[Device Setup](docs/DEVICE_SETUP.md)** - iOS and Android device configuration
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🔧 Configuration

### Test Execution
```bash
# iOS Simulator
pytest tests/ios/ --platform=ios_simulator

# iOS Real Device  
pytest tests/ios/ --platform=ios_device --device-id=YOUR_UDID

# Android Emulator
pytest tests/android/ --platform=android_emulator

# Android Real Device
pytest tests/android/ --platform=android_device --device-id=YOUR_DEVICE_ID

# Specific test markers
pytest tests/ -m smoke                    # Smoke tests only
pytest tests/ -m "ios and regression"     # iOS regression tests
pytest tests/ -n 2                        # Parallel execution
```

### Reports
```bash
# HTML Report
pytest tests/ --html=reports/report.html --self-contained-html

# Allure Report  
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 🛠️ Development

### Adding New Tests
1. Create page objects in `src/pages/`
2. Add test logic in `tests/shared/`
3. Create platform-specific tests in `tests/ios/` or `tests/android/`
4. Update configurations if needed

### Custom Test Data
```python
# In test files, override default data:
self.test_data.update({
    'password': 'CustomPassword123@',
    'first_name': 'Custom',
    'last_name': 'Name'
})
```

### Utilities
- **Phone Generator**: `src/utils/phone_generator.py` - Random phone number generation
- **SMS Helper**: `src/utils/sms_helper.py` - OTP verification code retrieval  
- **Device Helper**: `src/utils/device_helper.py` - Device management and information

## 📊 Test Markers

Use pytest markers to run specific test subsets:

- `@pytest.mark.ios` - iOS platform tests
- `@pytest.mark.android` - Android platform tests  
- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.device` - Real device tests
- `@pytest.mark.simulator` - Simulator/emulator tests

## 🔍 Debugging

### Screenshots
Screenshots are automatically captured at key steps and on failures in the `screenshots/` directory.

### Logs
```bash
# Verbose test output
pytest -s -v tests/

# Debug Appium communication
appium --log-level debug

# Device logs
adb logcat                    # Android
idevicesyslog                 # iOS
```

## 🚧 Continuous Integration

### GitHub Actions Example
```yaml
name: Mobile Tests
on: [push, pull_request]
jobs:
  ios-tests:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup environment
        run: |
          npm install -g appium
          appium driver install xcuitest
          pip install -r requirements.txt
      - name: Run tests
        run: |
          appium &
          pytest tests/ios/ -m smoke
```

## ⚡ Performance Tips

1. **Use specific locators** - ID > Accessibility ID > XPath
2. **Disable animations** - Set `disableWindowAnimation: true` for Android
3. **Optimize waits** - Use explicit waits over implicit waits
4. **Reset between tests** - Use `fullReset: true` for clean state
5. **Parallel execution** - Use `-n` flag with pytest-xdist

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add tests for new features
3. Update documentation for changes
4. Use meaningful commit messages
5. Test on both iOS and Android when possible

## 🔄 Migration from Maestro

This Appium test suite provides equivalent functionality to the original Maestro tests with these improvements:

- **Real Device Support** - Run on physical devices, not just simulators
- **Better Debugging** - Comprehensive logging and screenshots
- **Cross-Platform** - Single codebase for iOS and Android
- **CI/CD Integration** - Better support for continuous integration
- **Extensibility** - Easy to add new tests and functionality

## 📞 Support

For issues and questions:

1. Check [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Review [Setup Documentation](docs/SETUP.md)  
3. Search existing issues in the project repository
4. Contact the QA team with detailed error information

---

**Note**: This test suite is designed to work alongside the existing Maestro tests. Both can coexist in the same project structure.