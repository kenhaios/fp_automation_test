# 🎯 FasterPay Maestro Test Automation

A robust, scalable Maestro mobile automation framework designed for comprehensive testing of the FasterPay mobile application across iOS and Android platforms.

## 📁 Project Structure

```
maestro/
├── flows/
│   ├── quality-gates/          # Critical release tests
│   ├── features/              # Feature-based test organization
│   ├── shared-components/     # Reusable flow components
│   └── test-suites/           # Pre-defined test collections
├── configs/                   # Environment & device configurations
├── data/                      # Test data files
├── scripts/                   # Utility scripts & helpers
├── reports/                   # Test execution reports
├── screenshots/               # Test screenshots
├── docs/                      # Documentation
├── templates/                 # Test templates
├── Makefile                   # Common commands
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- [Maestro CLI](https://maestro.mobile.dev/) installed
- FasterPay mobile app builds (iOS/Android)
- Xcode (for iOS testing and app building)
- Make (for using Makefile commands)
- iOS Simulator (managed automatically)

### Setup
```bash
# Clone and navigate to maestro directory
cd maestro/

# Setup environment
make setup

# Build and copy your iOS app (see App Build Guide)
# Place FasterPay.app in build/staging/ directory

# Run smoke tests (automatically starts simulator & installs app)
make test-smoke-ios
```

### App Build Setup (Required for iOS Testing)
Before running iOS tests, you need to build and place the FasterPay iOS app:

1. **Build the app** using Xcode or command line
2. **Copy .app file** to the correct directory:
   ```bash
   # For staging tests (default)
   cp -R /path/to/FasterPay.app build/staging/
   
   # For dev tests  
   cp -R /path/to/FasterPay.app build/dev/
   ```
3. **Run tests** - the app will be automatically installed

📖 **See [App Build Guide](docs/APP_BUILD_GUIDE.md) for detailed instructions**

## 🎮 Common Commands

### Quality Gates
```bash
make test-smoke-ios          # iOS-specific smoke tests  
make test-smoke-android      # Android-specific smoke tests
make test-regression-mobile  # Daily regression suite for both platforms
```

### Suite-Based Testing
```bash
make test-ios SUITES="auth-ios"                    # Run iOS authentication suite
make test-android SUITES="auth-android"            # Run Android authentication suite
make test-ios SUITES="auth-ios,payment-ios"        # Run multiple iOS suites
make test-android SUITES="auth-android,payment-android" # Run multiple Android suites
```

### Environment Testing
```bash
ENV=dev make test-smoke-ios      # Development environment
ENV=staging make test-smoke-ios  # Staging environment (default)
ENV=prod make test-smoke-ios     # Production environment
```

## 📝 Writing Tests

### Platform Naming Convention

#### Cross-platform tests
- **Filename**: `feature-action.yaml` (no suffix)
- **Tags**: Include both `platform:ios` and `platform:android`

#### Platform-specific tests
- **iOS**: `feature-action-ios.yaml` with `platform:ios` tag
- **Android**: `feature-action-android.yaml` with `platform:android` tag

### Test Template
```yaml
name: "Feature Name - Action - Platform"
description: "What this test validates"
tags:
  - feature:feature-name
  - test-type:happy-path|negative|edge-case
  - priority:p0|p1|p2|p3
  - component:component-name
  - owner:team-name
  - platform:ios|android
env:
  VARIABLE_NAME: "value"
---
# Test steps here
- launchApp:
    appId: "${APP_ID}"
```

### Required Tags
- `feature`: Feature being tested (auth, payments, etc.)
- `test-type`: Type of test (happy-path, negative, edge-case)
- `priority`: Test priority (p0, p1, p2, p3)
- `platform`: Platform compatibility (ios, android, or both)

## 🔧 Scripts

### Test Runner
```bash
# Basic usage
./scripts/run-tests.sh staging smoke

# Advanced usage
./scripts/run-tests.sh dev by-tag "feature:auth and priority:p1"
```

### Tag Validation
```bash
# Validate all test tags
make validate-tags

# Or directly
python3 scripts/validate-tags.py
```

## 📊 Test Organization

### Quality Gates
- **smoke-suite.yaml**: Critical paths for release validation
- **smoke-suite-ios.yaml**: iOS-specific critical paths
- **daily-regression.yaml**: Comprehensive daily tests

### Feature Structure
```
flows/features/auth/
├── happy-path/
│   ├── sign-up-flow.yaml          # Cross-platform
│   ├── sign-up-flow-ios.yaml      # iOS specific
│   └── sign-in-ios.yaml           # iOS specific
├── negative/
└── edge-cases/
```

### Shared Components
- **auth/**: Authentication-related reusable flows
- **navigation/**: App navigation components
- **validations/**: Common validation components

## 🌍 Environment Configuration

### Available Environments
- **dev**: Development environment
- **staging**: Staging environment (default)
- **prod**: Production environment (read-only tests)

### Configuration Files
**iOS Configuration:**
- `configs/env-dev-ios.yaml`
- `configs/env-staging-ios.yaml` 
- `configs/env-prod-ios.yaml`

**Android Configuration:**
- `configs/env-dev-android.yaml`
- `configs/env-staging-android.yaml`
- `configs/env-prod-android.yaml`

## 📈 CI/CD Integration

The framework is designed for seamless CI/CD integration:

```bash
# Pre-merge validation
make test-smoke-ios
make test-smoke-android

# Release validation
make test-regression-mobile

# Platform-specific testing
make test-ios SUITES="auth-ios"
make test-android SUITES="auth-android"
```

## 🎯 Best Practices

1. **Use shared components** for common actions
2. **Tag tests properly** for easy filtering
3. **Follow naming conventions** for platform-specific tests
4. **Parameterize test data** using environment variables
5. **Write descriptive test names** and descriptions
6. **Add assertions liberally** - don't just navigate
7. **Keep flows focused** - one flow, one scenario

## 🆘 Troubleshooting

### Common Issues
- **App not found error**: Build and copy .app file to build/ directory (see App Build Guide)
- **No iOS simulator running**: Run `make check-ios-simulator` to start one automatically
- **App not launching**: Check APP_ID in environment config
- **Element not found**: Verify element IDs in app
- **Tests flaky**: Add appropriate waits and retries

### Getting Help
```bash
make help                    # Show all available commands
make test-ios               # Show available iOS test suites (when run without SUITES)
make test-android           # Show available Android test suites (when run without SUITES)
```

## 📚 Documentation

- [App Build Guide](docs/APP_BUILD_GUIDE.md) - **Required for iOS testing**
- [Quick Start Guide](docs/QUICK_START.md)
- [Platform Conventions](docs/PLATFORM_CONVENTIONS.md)

## 🤝 Contributing

1. Follow the platform naming conventions
2. Add proper tags to all tests
3. Validate tags before committing: `make validate-tags`
4. Run smoke tests: `make test-smoke`
5. Update documentation as needed

---