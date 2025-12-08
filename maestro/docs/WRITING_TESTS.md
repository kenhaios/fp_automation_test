# 📝 Writing Tests with Maestro Studio

A complete step-by-step guide to creating robust mobile tests using Maestro Studio's interactive development environment.

## 📋 Prerequisites

### Required Software
- [Maestro CLI](https://maestro.mobile.dev/getting-started/installing-maestro) installed
- **Maestro Studio** (we'll download this in Step 1)
- iOS Simulator or Android Emulator
- FasterPay mobile app builds
- Text editor or IDE

### Knowledge Requirements
- Basic understanding of mobile UI testing
- Familiarity with YAML syntax
- Understanding of iOS/Android UI differences

---

## 🎯 Step-by-Step Test Development Process

### Step 1: Download & Install Maestro Studio

Maestro Studio is a visual tool that helps you write tests interactively by connecting to your device and recording actions.

```bash
# Download Maestro Studio (if not already installed)
maestro download-samples
maestro studio --help

# Alternative: Download from official releases
# Visit: https://github.com/mobile-dev-inc/maestro/releases
```

### Step 2: Create Test File from Template

Choose the appropriate template based on your target platform:

```bash
# Navigate to your test directory
cd maestro/flows/features/

# Create feature directory (if it doesn't exist)
mkdir -p my-feature/happy-path

# Copy platform-specific template
# For iOS:
cp ../../templates/test-template-ios.yaml my-feature/happy-path/my-test-ios.yaml

# For Android:
cp ../../templates/test-template-android.yaml my-feature/happy-path/my-test-android.yaml
```

**Edit your template file:**
```yaml
# Example: login-test-ios.yaml
name: "User Login - Happy Path - iOS"
description: "Test successful user login with valid credentials on iOS"
tags:
  - feature:auth
  - test-type:happy-path
  - priority:p1
  - component:login
  - owner:qa-team
  - platform:ios
env:
  USERNAME: "${TEST_USER}"
  PASSWORD: "${TEST_PASSWORD}"
appId: ${APP_ID}
---
# Test steps will be written using Maestro Studio
```

### Step 3: Start iOS Simulator or Android Emulator

#### For iOS Testing:
```bash
# Automatic simulator management
make check-ios-simulator

# Manual simulator start
open -a Simulator
# Or use Xcode → Open Developer Tool → Simulator
```

#### For Android Testing:
```bash
# Start Android emulator
emulator -avd YOUR_AVD_NAME

# List available AVDs
emulator -list-avds

# Create new AVD if needed
avdmanager create avd -n "Pixel_7_API_34" -k "system-images;android-34;google_apis;x86_64"
```

### Step 4: Install and Launch Your App

#### For iOS:
```bash
# Install app using Makefile (recommended)
make install-app ENV=staging

# Manual installation
xcrun simctl install booted build/staging/FasterPay.app
xcrun simctl launch booted com.fasterpay.app.staging
```

#### For Android:
```bash
# Install APK
adb install path/to/FasterPay.apk

# Launch app
adb shell am start -n com.fasterpay.ewallet/.MainActivity
```

### Step 5: Launch Maestro Studio

```bash
# Start Maestro Studio
maestro studio

# Maestro Studio will open in your browser at http://localhost:9999
```

**What you'll see in Maestro Studio:**
- 📱 Device screen mirroring
- 🎯 Element inspector
- ⌨️ Command palette
- 📝 Test recorder
- 🔍 Element selector tools

### Step 6: Connect Maestro Studio to Device

1. **In Maestro Studio browser window:**
   - Click "Connect to Device"
   - Select your iOS Simulator or Android Emulator
   - You should see your device screen appear in the browser

2. **Verify connection:**
   - Try tapping on elements in the Studio interface
   - Verify actions are reflected on your device
   - Check that element highlighting works

### Step 7: Write and Test Steps Interactively

Now comes the interactive magic! Use Maestro Studio to build your test step by step.

#### 7.1 Record Basic Actions

**In Maestro Studio:**

1. **Enable Recording Mode**
   - Click the "🔴 Record" button
   - All your taps and inputs will be captured

2. **Perform Your Test Flow**
   - Navigate to login screen
   - Enter credentials
   - Submit form
   - Verify success

3. **View Generated Commands**
   - Studio shows generated YAML in real-time
   - Commands appear as you perform actions

#### 7.2 Refine Element Selectors

**Use the Element Inspector:**

1. **Click "🎯 Inspect Element"**
2. **Tap any element on the screen**
3. **Review available selectors:**
   ```yaml
   # Studio will show options like:
   - tapOn: "Login"                    # Text-based
   - tapOn: { id: "loginButton" }      # ID-based  
   - tapOn: { accessibilityId: "login" } # Accessibility
   - tapOn: { xpath: "//Button[@text='Login']" } # XPath
   ```

4. **Choose the most reliable selector:**
   - ✅ Prefer IDs and accessibility IDs
   - ✅ Use text for stable UI elements
   - ⚠️ Use XPath sparingly (brittle)

#### 7.3 Add Assertions and Waits

**Test your assertions in real-time:**

```yaml
# Wait for elements to appear
- extendedWaitUntil:
    visible: "Welcome back"
    timeout: 10000

# Assert critical elements
- assertVisible: "Dashboard"
- assertNotVisible: "Loading..."

# Test these in Studio before adding to your file
```


### Step 8: Export and Refine Test File

#### 8.1 Export from Studio

1. **Copy generated commands from Studio**
2. **Paste into your test file**
3. **Clean up and organize:**

```yaml
name: "User Login - Happy Path - iOS"
description: "Test successful user login with valid credentials"
tags:
  - feature:auth
  - test-type:happy-path
  - priority:p1
  - component:login
  - owner:qa-team
  - platform:ios
env:
  USERNAME: "${TEST_USER}"
  PASSWORD: "${TEST_PASSWORD}"
appId: ${APP_ID}
---
# Cleaned up commands from Studio
- launchApp:
    appId: "${APP_ID}"

- tapOn: "Log In"

- tapOn:
    id: "emailField"
- inputText: "${USERNAME}"

- tapOn:
    id: "passwordField"  
- inputText: "${PASSWORD}"

- tapOn: "Sign In"

- extendedWaitUntil:
    visible: "Dashboard"
    timeout: 15000

- assertVisible: "Welcome back"
```

#### 8.2 Test Your File

```bash
# Test the individual file
maestro test flows/features/auth/happy-path/login-test-ios.yaml \
  -e APP_ID=com.fasterpay.app.staging \
  -e TEST_USER="test@example.com" \
  -e TEST_PASSWORD="password123"

# Test with environment file
maestro test flows/features/auth/happy-path/login-test-ios.yaml \
  $(make -s extract-env-vars ENV=staging PLATFORM=ios)
```

### Step 9: Create Test Suite for Feature

Once you have individual test files working, organize them into a test suite.

#### 9.1 Create Test Suite File

```bash
# Create feature test suite
touch flows/test-suites/auth-ios.yaml
```

#### 9.2 Define Test Suite

```yaml
# flows/test-suites/auth-ios.yaml
name: "Authentication Test Suite - iOS"
description: "Complete authentication testing for iOS platform"
tags:
  - test-suite
  - feature:auth
  - platform:ios
env:
  APP_ID: com.fasterpay.app.staging
  TEST_USER: iosus02@fp.com
  TEST_PASSWORD: "12345Aa@"
appId: ${APP_ID}
---
# Happy Path Tests
- runFlow: ../features/auth/happy-path/login-test-ios.yaml
- runFlow: ../features/auth/happy-path/signup-test-ios.yaml
- runFlow: ../features/auth/happy-path/logout-test-ios.yaml

# Negative Tests  
- runFlow: ../features/auth/negative/invalid-login-ios.yaml
- runFlow: ../features/auth/negative/expired-session-ios.yaml

# Edge Cases
- runFlow: ../features/auth/edge-cases/network-failure-ios.yaml
```

#### 9.3 Test Complete Suite

```bash
# Test using Makefile
make test-ios SUITES="auth-ios" ENV=staging

# Direct test
maestro test flows/test-suites/auth-ios.yaml \
  $(make -s extract-env-vars ENV=staging PLATFORM=ios)
```

---

## 🎨 Maestro Studio Best Practices

### Visual Element Selection

**Use Studio's visual tools effectively:**

1. **Hierarchy View**
   - Explore element tree structure
   - Find parent/child relationships
   - Identify unique attributes

2. **Element Properties Panel**
   - Review all available attributes
   - Check text, ID, accessibility properties
   - Note platform-specific attributes

3. **Selector Testing**
   - Test selectors before using them
   - Verify they work across different screens
   - Check selector stability

### Recording Techniques

**Best practices for recording:**

1. **Record in Small Chunks**
   - Record 3-5 actions at a time
   - Review and clean up frequently
   - Avoid long recording sessions

2. **Include Waits and Assertions**
   - Add waits for dynamic content
   - Assert critical state changes
   - Verify user feedback elements

3. **Handle Dynamic Content**
   - Use proper waits for loading states
   - Account for animation timing
   - Test with different data

---

## 🏗️ Test File Structure Best Practices

### Essential Components

Every test should include:

```yaml
# 1. Clear metadata
name: "Clear, descriptive test name"
description: "What this test validates and expected outcome"
tags:
  - feature:feature-name      # Required
  - test-type:happy-path     # Required
  - priority:p1              # Required  
  - component:component-name # Required
  - owner:team-name         # Required
  - platform:ios            # Required

# 2. Environment variables
env:
  VARIABLE_NAME: "value"
  DYNAMIC_VALUE: "${ENV_VARIABLE}"

# 3. App identifier
appId: ${APP_ID}

# 4. Separator
---

# 5. Test steps
- launchApp:
    appId: "${APP_ID}"
# ... rest of test steps
```

### Step Organization

**Structure your test steps logically:**

```yaml
---
# 1. Setup and navigation
- launchApp:
    appId: "${APP_ID}"
- tapOn: "Get Started"

# 2. Main test actions  
- tapOn: "Login"
- inputText: "${USERNAME}"
- tapOn: "Submit"

# 3. Verification
- extendedWaitUntil:
    visible: "Success"
    timeout: 10000
- assertVisible: "Dashboard"

# 4. Cleanup (if needed)
- tapOn: "Logout"
```

---

## 🔧 Platform-Specific Guidance

### iOS-Specific Considerations

**Use Studio to identify iOS elements:**

```yaml
# iOS Navigation Controllers
- tapOn:
    xpath: "//XCUIElementTypeNavigationBar[@name='Settings']"

# iOS Alerts
- tapOn:
    xpath: "//XCUIElementTypeAlert//XCUIElementTypeButton[@name='Allow']"

# iOS Switches
- tapOn:
    xpath: "//XCUIElementTypeSwitch[@name='Enable Notifications']"

# iOS Pickers
- tapOn:
    xpath: "//XCUIElementTypePickerWheel"
- scroll:
    element:
      xpath: "//XCUIElementTypePickerWheel"
    direction: UP
```

**iOS Studio Tips:**
- Use accessibility inspector alongside Studio
- Test with different iOS versions
- Account for safe area differences
- Handle iOS permission dialogs

### Android-Specific Considerations

**Use Studio to identify Android elements:**

```yaml
# Material Design Components
- tapOn:
    xpath: "//com.google.android.material.button.MaterialButton[@text='Submit']"

# RecyclerView Items  
- tapOn:
    xpath: "//androidx.recyclerview.widget.RecyclerView//android.widget.TextView[@text='Item']"

# Navigation Drawer
- swipe:
    direction: RIGHT
    element:
      xpath: "//androidx.drawerlayout.widget.DrawerLayout"

# Hardware Buttons
- pressKey: Back
- pressKey: Home
```

**Android Studio Tips:**
- Use Layout Inspector alongside Studio
- Test with different API levels
- Handle Android permission models
- Account for different screen densities

---

## 🔍 Element Selection Best Practices

### Selector Priority (Most Reliable → Least Reliable)

1. **ID Selectors** ✅ Most Reliable
   ```yaml
   - tapOn:
       id: "uniqueElementId"
   ```

2. **Accessibility ID** ✅ Very Reliable
   ```yaml
   - tapOn:
       accessibilityId: "loginButton"
   ```

3. **Text Content** ⚠️ Moderately Reliable
   ```yaml
   - tapOn: "Submit"  # Good for buttons with static text
   ```

4. **XPath Selectors** ⚠️ Use Sparingly
   ```yaml
   - tapOn:
       xpath: "//Button[@text='Submit' and @enabled='true']"
   ```

### Using Studio for Selector Validation

**Test selector reliability in Studio:**

1. **Multi-Screen Testing**
   - Navigate to different screens
   - Verify selector still works
   - Check for selector conflicts

2. **Data Variation Testing**
   - Test with different user data
   - Verify selectors handle dynamic content
   - Check with empty/full states

3. **Timing Testing**
   - Test selectors after animations
   - Verify they work during loading states
   - Check timing-dependent selectors

---

## 🧪 Testing Your Tests

### Individual Test Validation

**Test each file thoroughly:**

```bash
# Quick test
maestro test my-test.yaml

# Test with debug output
maestro test my-test.yaml

# Test with different data
maestro test my-test.yaml \
  -e TEST_USER="different@user.com" \
  -e TEST_PASSWORD="differentpass"
```

### Suite Integration Testing

**Validate test suites:**

```bash
# Test complete suite
make test-ios SUITES="auth-ios" ENV=staging

# Test suite components individually
maestro test flows/test-suites/auth-ios.yaml

# Test with different environments
make test-ios SUITES="auth-ios" ENV=dev
make test-ios SUITES="auth-ios" ENV=prod
```

### Continuous Testing

**Set up regular validation:**

```bash
# Daily smoke test
make test-smoke-ios

# Weekly full regression
make test-regression-mobile

# Pre-commit validation
make validate-tags
```

---

## 🚨 Troubleshooting Common Issues

### Studio Connection Issues

**Problem:** Studio can't connect to device
```bash
# Solution 1: Restart Studio
killall maestro-studio
maestro studio

# Solution 2: Reset device connection
maestro studio --reset-device

# Solution 3: Check device status
maestro studio --list-devices
```

**Problem:** Device screen not showing in Studio
```bash
# For iOS: Restart simulator
xcrun simctl shutdown all
xcrun simctl boot "YOUR_DEVICE_ID"

# For Android: Restart emulator
adb kill-server
adb start-server
```

### Element Selection Issues

**Problem:** Elements not found during recording

1. **Wait for elements to load:**
   ```yaml
   - extendedWaitUntil:
       visible: "ElementText"
       timeout: 10000
   ```

2. **Use more specific selectors:**
   ```yaml
   # Instead of:
   - tapOn: "Submit"
   
   # Use:
   - tapOn:
       id: "submitButton"
   ```

3. **Check element hierarchy:**
   - Use Studio's inspector
   - Look for parent elements
   - Find unique attributes

### Test Flakiness

**Problem:** Tests pass sometimes, fail others

**Solutions:**

1. **Add appropriate waits:**
   ```yaml
   # Wait for animations
   - extendedWaitUntil:
       visible: "ExpectedElement"
       timeout: 15000
   
   # Add delays for transitions
   - delay: 2000
   ```

2. **Use retry mechanisms:**
   ```yaml
   - repeat:
       times: 3
       commands:
         - tapOn: "RefreshButton"
         - extendedWaitUntil:
             visible: "LoadedContent"
             timeout: 5000
   ```

3. **Handle dynamic content:**
   ```yaml
   # Use optional elements
   - tapOn:
       text: "OptionalButton"
       optional: true
   
   # Handle multiple scenarios
   - runFlow:
       when:
         visible: "DialogTitle"
       file: handle-dialog.yaml
   ```

---

## 📚 Advanced Topics

### Using Shared Components

**Create reusable flows:**

```yaml
# flows/shared-components/auth/login-flow.yaml
name: "Login Flow - Shared Component"
tags:
  - shared
  - auth
env:
  USERNAME: "${TEST_USER}"
  PASSWORD: "${TEST_PASSWORD}"
---
- tapOn: "Login"
- tapOn:
    id: "emailField"
- inputText: "${USERNAME}"
- tapOn:
    id: "passwordField"
- inputText: "${PASSWORD}"
- tapOn: "Submit"
- extendedWaitUntil:
    visible: "Dashboard"
    timeout: 15000
```

**Use in your tests:**
```yaml
# In your main test
- runFlow: ../../shared-components/auth/login-flow.yaml
```

### Environment Variables and Configuration

**Leverage environment-specific settings:**

```yaml
# In your test
env:
  BASE_URL: "${API_BASE_URL}"
  TIMEOUT: "${DEFAULT_TIMEOUT}"
  TEST_DATA: "${FEATURE_TEST_DATA}"

# Use throughout test
- extendedWaitUntil:
    visible: "Content"
    timeout: ${TIMEOUT}
```

### Complex User Flows

**Handle multi-step scenarios:**

```yaml
# Example: Complete user onboarding
---
- runFlow: ../shared-components/auth/signup-flow.yaml
- runFlow: ../shared-components/onboarding/verify-email.yaml
- runFlow: ../shared-components/onboarding/setup-profile.yaml
- runFlow: ../shared-components/onboarding/enable-notifications.yaml
- runFlow: ../shared-components/validation/assert-onboarding-complete.yaml
```

### Error Handling and Recovery

**Build robust tests with error handling:**

```yaml
# Handle expected errors gracefully
- runFlow:
    when:
      visible: "Error Message"
    file: ../shared-components/error/handle-network-error.yaml

# Retry failed operations
- repeat:
    times: 3
    commands:
      - tapOn: "RetryButton"
      - extendedWaitUntil:
          visible: "SuccessMessage"
          timeout: 10000
```
