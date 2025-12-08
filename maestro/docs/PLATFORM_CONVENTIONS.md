# 📱 Platform Conventions Guide

Understanding how to structure tests for iOS, Android, and cross-platform scenarios in the FasterPay Maestro automation framework.

## 🎯 Platform Strategy Overview

Our framework supports three types of tests:
1. **Cross-platform tests**: Work on both iOS and Android
2. **iOS-specific tests**: Only for iOS devices
3. **Android-specific tests**: Only for Android devices

## 📝 Naming Conventions

### File Naming Rules

#### Cross-Platform Tests
```
✅ CORRECT: sign-up-flow.yaml
❌ WRONG:   sign-up-flow-cross.yaml
❌ WRONG:   sign-up-flow-both.yaml

# Tags required:
tags:
  - platform:ios
  - platform:android
```

#### iOS-Specific Tests
```
✅ CORRECT: sign-up-flow-ios.yaml
❌ WRONG:   sign-up-flow.ios.yaml
❌ WRONG:   ios-sign-up-flow.yaml

# Tags required:
tags:
  - platform:ios
```

#### Android-Specific Tests
```
✅ CORRECT: sign-up-flow-android.yaml
❌ WRONG:   sign-up-flow.android.yaml
❌ WRONG:   android-sign-up-flow.yaml

# Tags required:
tags:
  - platform:android
```

## 🏗️ Test Structure Examples

### Cross-Platform Test Template
```yaml
# flows/features/auth/happy-path/login-user.yaml
name: "User Login - Happy Path - Cross Platform"
description: "Standard user login flow that works on both platforms"
tags:
  - feature:auth
  - test-type:happy-path
  - priority:p1
  - component:login
  - owner:auth-team
  - platform:ios
  - platform:android
env:
  USERNAME: "${TEST_USER}"
  PASSWORD: "${TEST_PASSWORD}"
---
- runFlow: ../../shared-components/navigation/app-launch.yaml
- tapOn: "Login"
- tapOn:
    id: usernameField  # Works on both platforms
- inputText: "${USERNAME}"
- tapOn:
    id: passwordField  # Works on both platforms
- inputText: "${PASSWORD}"
- tapOn: "Sign In"
- runFlow: ../../shared-components/validations/assert-home-screen.yaml
```

### iOS-Specific Test Template
```yaml
# flows/features/auth/happy-path/biometric-login-ios.yaml
name: "Biometric Login - iOS Specific"
description: "Face ID/Touch ID authentication flow for iOS"
tags:
  - feature:auth
  - test-type:happy-path
  - priority:p2
  - component:biometric
  - owner:auth-team
  - platform:ios
---
- runFlow: ../../shared-components/navigation/app-launch.yaml
- tapOn: "Login"
- tapOn: "Use Face ID"
# iOS-specific biometric simulation
- tapOn:
    id: biometricPrompt
- assertVisible: "Face ID Successful"
- runFlow: ../../shared-components/validations/assert-home-screen.yaml
```

### Android-Specific Test Template
```yaml
# flows/features/auth/happy-path/fingerprint-login-android.yaml
name: "Fingerprint Login - Android Specific"
description: "Fingerprint authentication flow for Android"
tags:
  - feature:auth
  - test-type:happy-path
  - priority:p2
  - component:biometric
  - owner:auth-team
  - platform:android
---
- runFlow: ../../shared-components/navigation/app-launch.yaml
- tapOn: "Login"
- tapOn: "Use Fingerprint"
# Android-specific fingerprint simulation
- tapOn:
    id: fingerprintSensor
- assertVisible: "Fingerprint Verified"
- runFlow: ../../shared-components/validations/assert-home-screen.yaml
```

## 🎭 When to Use Each Type

### Cross-Platform Tests ✅
Use when:
- Core functionality works identically on both platforms
- UI elements have the same IDs/text
- User flows are identical
- Business logic is the same

**Examples:**
- Basic login/signup flows
- Standard navigation
- Form submissions with common fields
- API-driven content display

### iOS-Specific Tests 🍎
Use when:
- iOS-specific UI patterns (navigation controllers, alerts)
- iOS-exclusive features (Face ID, Touch ID, 3D Touch)
- iOS-specific system integrations
- Different UI element behavior

**Examples:**
- Face ID/Touch ID authentication
- iOS native alerts and action sheets
- Swipe gestures with iOS-specific behavior
- iOS-specific accessibility features

### Android-Specific Tests 🤖
Use when:
- Android-specific UI patterns (fragments, material design)
- Android-exclusive features (fingerprint, back button)
- Android-specific system integrations
- Different UI element behavior

**Examples:**
- Fingerprint authentication
- Hardware back button navigation
- Android-specific notifications
- Material Design specific interactions

## 🔍 Element Selection Strategies

### Cross-Platform Element Selection
```yaml
# Prefer IDs that work on both platforms
- tapOn:
    id: submitButton  # Same ID on both platforms

# Use consistent text
- tapOn: "Continue"  # Same button text on both platforms

# Use accessibility labels
- tapOn:
    accessibilityId: loginButton
```

### Platform-Specific Element Selection
```yaml
# iOS-specific selectors
- tapOn:
    xpath: "//XCUIElementTypeButton[@name='iOS Submit']"

# Android-specific selectors  
- tapOn:
    xpath: "//android.widget.Button[@text='Android Submit']"

# Platform-specific IDs
- tapOn:
    id: iosSpecificButtonId  # Only exists on iOS
```

## 📊 Test Execution Strategies

### Running Suite-Based Tests
```bash
# Run specific iOS test suites
make test-ios SUITES="auth-ios"
make test-ios SUITES="auth-ios,payment-ios"

# Run specific Android test suites
make test-android SUITES="auth-android"
make test-android SUITES="auth-android,payment-android"

# List available suites (run without SUITES parameter)
make test-ios        # Shows all available iOS test suites
make test-android    # Shows all available Android test suites
```

### Running Platform-Specific Tests
```bash
# Run individual test files directly
maestro test flows/features/auth/happy-path/login-user-ios.yaml
maestro test flows/features/auth/happy-path/login-user-android.yaml

# Run test suites with environment variables
ENV=staging make test-ios SUITES="auth-ios"
ENV=dev make test-android SUITES="auth-android"
```

### Quality Gate Execution
```bash
# Run platform-specific smoke tests
make test-smoke-ios
make test-smoke-android

# Run comprehensive regression testing
make test-regression-mobile  # Runs both iOS and Android regression suites
```

## 🏷️ Tagging Best Practices

### Required Platform Tags
```yaml
# Cross-platform
tags:
  - platform:ios
  - platform:android

# iOS only
tags:
  - platform:ios

# Android only
tags:
  - platform:android
```

### Additional Recommended Tags
```yaml
tags:
  - feature:auth
  - test-type:happy-path
  - priority:p1
  - component:login
  - owner:auth-team
  - platform:ios
  - device-type:simulator    # or real-device
  - ios-version:17.0         # for iOS-specific tests
  - android-api:34           # for Android-specific tests
```

## 🔧 Shared Components Strategy

### Cross-Platform Shared Components
```yaml
# flows/shared-components/auth/logout-flow.yaml
name: "Logout Flow - Cross Platform"
tags:
  - shared
  - auth
  - platform:ios
  - platform:android
---
- tapOn:
    id: settingsButton  # Same ID on both platforms
- tapOn: "Logout"       # Same text on both platforms
- tapOn: "Confirm"      # Same confirmation flow
```

### Platform-Specific Shared Components
```yaml
# flows/shared-components/auth/logout-flow-ios.yaml
name: "Logout Flow - iOS Specific"
tags:
  - shared
  - auth
  - platform:ios
---
- tapOn:
    id: settingsButton
- tapOn: "Logout"
# iOS-specific confirmation alert
- tapOn:
    xpath: "//XCUIElementTypeAlert//XCUIElementTypeButton[@name='Logout']"
```

## 📈 Quality Gates Strategy

### Test Suite Organization
```yaml
# flows/test-suites/auth-ios.yaml
name: "Authentication Test Suite - iOS Specific"
tags:
  - test-suite
  - feature:auth
  - platform:ios
env:
  APP_ID: com.fasterpay.app.staging
  TEST_USER: iosus02@fp.com
  TEST_PASSWORD: "12345Aa@"
---
- runFlow: ../features/auth/happy-path/sign-up-flow-ios.yaml
- runFlow: ../features/auth/happy-path/biometric-login-ios.yaml
```

```yaml
# flows/test-suites/auth-android.yaml
name: "Authentication Test Suite - Android Specific"
tags:
  - test-suite
  - feature:auth
  - platform:android
env:
  APP_ID: com.fasterpay.ewallet
  TEST_USER: iosus02@fp.com
  TEST_PASSWORD: "12345Aa@"
---
- runFlow: ../features/auth/happy-path/sign-up-flow-android.yaml
- runFlow: ../features/auth/happy-path/fingerprint-login-android.yaml
```

### Quality Gate Test Suites
```yaml
# flows/quality-gates/smoke-suite-ios.yaml
name: "Smoke Test Suite - iOS"
tags:
  - quality-gate
  - platform:ios
---
- runFlow: ../features/auth/happy-path/sign-up-flow-ios.yaml
- runFlow: ../features/auth/happy-path/biometric-login-ios.yaml
```

## ⚠️ Common Pitfalls

### ❌ Don't Do This
```yaml
# Wrong: Platform logic inside cross-platform test
- if:
    platform: ios
    command:
      - tapOn: "iOS Button"
- if:
    platform: android  
    command:
      - tapOn: "Android Button"
```

### ✅ Do This Instead
```yaml
# Correct: Separate platform-specific tests
# File: feature-action-ios.yaml
- tapOn: "iOS Button"

# File: feature-action-android.yaml  
- tapOn: "Android Button"
```

### ❌ Wrong File Naming
```
sign-up-ios.yaml          # Missing flow description
ios_sign_up_flow.yaml     # Wrong separator
signUpFlow-iOS.yaml       # Wrong case and separator
```

### ✅ Correct File Naming
```
sign-up-flow-ios.yaml     # Correct: action-description-platform.yaml
payment-flow-android.yaml # Correct: feature-flow-platform.yaml
login-user.yaml           # Correct: cross-platform (no suffix)
```

## 📚 References

- [Test Templates](../templates/) - Ready-to-use templates
- [Shared Components](../flows/shared-components/) - Reusable flows
- [Quality Gates](QUALITY_GATES.md) - Understanding test organization
- [Writing Tests](WRITING_TESTS.md) - Detailed test creation guide

---

🎯 **Remember**: The goal is to maximize test reuse while maintaining platform-specific testing where needed.