# 🚀 Quick Start Guide

Get up and running with FasterPay Maestro automation in minutes.

## Prerequisites

### Required Software
- [Maestro CLI](https://maestro.mobile.dev/getting-started/installing-maestro)
- iOS Simulator / Android Emulator or physical devices
- FasterPay mobile app installed
- Make utility (usually pre-installed on macOS/Linux)

### Installation
```bash
# Install Maestro CLI
curl -Ls "https://get.maestro.mobile.dev" | bash

# Verify installation
maestro --version
```

## First Test Run

### 1. Navigate to Maestro Directory
```bash
cd /path/to/fp_automation_test/maestro/
```

### 2. Setup Environment
```bash
make setup
```

### 3. Run Your First Test
```bash
# Quick smoke test for iOS
make test-smoke-ios

# Quick smoke test for Android
make test-smoke-android

# Or run a specific test
maestro test flows/features/auth/happy-path/sign-up-flow.yaml
```

## Understanding the Output

### Successful Test
```
✅ Flow completed successfully
📊 3 steps completed in 45.2s
📁 Screenshots saved to: screenshots/
```

### Failed Test
```
❌ Flow failed at step 5
🔍 Element not found: "Sign Up Button"
📸 Failure screenshot: screenshots/failure_timestamp.png
```

## Common Commands

### Quality Gates (Most Important)
```bash
make test-smoke-ios          # 🔥 Run iOS critical path tests
make test-smoke-android      # 🔥 Run Android critical path tests
make test-regression-mobile  # 📊 Run comprehensive daily tests for both platforms
```

### Development Testing
```bash
make quick-auth             # ⚡ Super quick auth check
make quick-ios              # ⚡ Quick iOS validation
ENV=dev make test-smoke-ios # 🛠️ Test iOS on development environment
ENV=dev make test-smoke-android # 🛠️ Test Android on development environment
```

### Suite-Based Testing
```bash
make test-ios SUITES="auth-ios"              # 🍎 Run iOS authentication suite
make test-android SUITES="auth-android"      # 🤖 Run Android authentication suite
make test-ios SUITES="auth-ios,payment-ios"  # 🍎 Run multiple iOS suites
make test-ios                               # 🍎 List available iOS suites
make test-android                           # 🤖 List available Android suites
```

## Environment Selection

### Available Environments
- **dev**: Development environment (fast, less stable)
- **staging**: Staging environment (default, stable)  
- **prod**: Production environment (read-only, most stable)

### Usage
```bash
# Default (staging)
make test-smoke-ios

# Specific environment
ENV=dev make test-smoke-ios
ENV=prod make test-smoke-ios

# Android testing
ENV=dev make test-smoke-android
ENV=staging make test-smoke-android
```

## Your First Custom Test

### 1. Choose Template
```bash
# Cross-platform test
cp templates/test-template.yaml flows/features/my-feature/happy-path/my-test.yaml

# iOS-specific test  
cp templates/test-template-ios.yaml flows/features/my-feature/happy-path/my-test-ios.yaml
```

### 2. Edit Your Test
```yaml
name: "My Feature - Happy Path"
description: "Test my awesome feature"
tags:
  - feature:my-feature
  - test-type:happy-path
  - priority:p1
  - component:my-component
  - owner:my-team
  - platform:ios
  - platform:android
---
- runFlow: ../../shared-components/navigation/app-launch.yaml
- tapOn: "My Button"
- assertVisible: "Success Message"
```

### 3. Test Your Flow
```bash
maestro test flows/features/my-feature/happy-path/my-test.yaml
```

## Troubleshooting Quick Fixes

### App Won't Launch
```bash
# Check if app is installed
maestro studio

# Verify app ID in configs/env-staging.yaml
# Should match your app's bundle identifier
```

### Element Not Found
```bash
# Use Maestro Studio to inspect elements
maestro studio

# Add waits for dynamic content
- extendedWaitUntil:
    visible: "Element Name"
    timeout: 10000
```

### Tests Are Flaky
```bash
# Add delays between actions
- tapOn: "Button"
- delay: 1000
- assertVisible: "Result"

# Or use retries
- repeat:
    times: 3
    commands:
      - tapOn: "Refresh"
      - assertVisible: "Content"
```

## Next Steps

### Learn More
1. [Writing Tests](WRITING_TESTS.md) - Detailed test creation guide
2. [Platform Conventions](PLATFORM_CONVENTIONS.md) - iOS vs Android guidelines
3. [Quality Gates](QUALITY_GATES.md) - Understanding test organization

### Validate Your Setup
```bash
# Check if all tags are correct
make validate-tags

# Run test suites
make test-ios SUITES="auth-ios"
make test-android SUITES="auth-android"

# Generate test reports
make test-smoke-ios ENV=staging
make test-smoke-android ENV=staging
```

## Getting Help

### Available Commands
```bash
make help                    # Show all available commands
make test-ios               # Show available iOS test suites
make test-android           # Show available Android test suites
```

### Common File Locations
- **Test files**: `flows/features/`
- **Shared components**: `flows/shared-components/`
- **Environment configs**: `configs/`
- **Reports**: `reports/`
- **Screenshots**: `screenshots/`

### Support
- Check existing tests in `flows/features/auth/happy-path/` for examples
- Run `maestro --help` for CLI documentation
- Use `maestro studio` for interactive app exploration

---

🎉 **Congratulations!** You're now ready to create robust mobile tests with Maestro.