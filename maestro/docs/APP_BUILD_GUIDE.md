# App Build Guide for Maestro Testing

This guide explains how to build and prepare iOS app builds for automated testing with Maestro.

## Overview

The Maestro test framework requires the actual iOS app (.app file) to be installed on the simulator before running tests. This guide covers:

1. Building the FasterPay iOS app for different environments
2. Placing app builds in the correct location
3. Running tests with automatic app installation

## Prerequisites

- Xcode installed with iOS SDK
- FasterPay iOS project source code
- iOS Simulator available
- Maestro CLI installed

## Building the App

### Environment Configurations

The FasterPay app supports three environments:
- **staging**: For testing against staging APIs
- **dev**: For development testing  
- **prod**: For production testing (use with caution)

### Build Steps

#### Option 1: Xcode GUI Build

1. **Open the project** in Xcode
2. **Select the target scheme**:
   - For staging: Select "FasterPay-Staging" scheme
   - For dev: Select "FasterPay-Dev" scheme  
   - For prod: Select "FasterPay-Prod" scheme
3. **Select simulator destination**: Choose "Any iOS Simulator"
4. **Build the project**: Product → Build (⌘+B)
5. **Find the .app file**:
   - Open the Products folder in Xcode navigator
   - Right-click on "FasterPay.app" → Show in Finder
   - Copy the entire .app folder

#### Option 2: Command Line Build

```bash
# Navigate to project directory
cd /path/to/fasterpay-ios-project

# Build for staging
xcodebuild -scheme FasterPay-Staging -destination "generic/platform=iOS Simulator" -derivedDataPath ./build

# Build for dev  
xcodebuild -scheme FasterPay-Dev -destination "generic/platform=iOS Simulator" -derivedDataPath ./build

# Build for prod
xcodebuild -scheme FasterPay-Prod -destination "generic/platform=iOS Simulator" -derivedDataPath ./build
```

The .app file will be located in:
```
./build/Build/Products/Debug-iphonesimulator/FasterPay.app
```

## App Installation

### Directory Structure

Copy your built .app file to the appropriate directory in the Maestro project:

```
maestro/
├── build/
│   ├── staging/
│   │   └── FasterPay.app     # Staging build
│   ├── dev/
│   │   └── FasterPay.app     # Dev build
│   └── prod/
│       └── FasterPay.app     # Prod build
```

### Copy Commands

```bash
# From your iOS project build directory
cd /path/to/fasterpay-ios-project

# Copy staging build
cp -R ./build/Build/Products/Debug-iphonesimulator/FasterPay.app /path/to/maestro/build/staging/

# Copy dev build  
cp -R ./build/Build/Products/Debug-iphonesimulator/FasterPay.app /path/to/maestro/build/dev/

# Copy prod build
cp -R ./build/Build/Products/Debug-iphonesimulator/FasterPay.app /path/to/maestro/build/prod/
```

## Running Tests

### Automatic Installation and Testing

Once your .app file is in place, the Maestro framework will automatically:
1. Start the appropriate iOS simulator 
2. Install the app for your target environment
3. Run the tests

```bash
# Run staging tests (default)
make test-smoke-ios

# Run dev tests
make test-smoke-ios ENV=dev

# Run prod tests  
make test-smoke-ios ENV=prod
```

### Manual App Installation

You can also install the app manually without running tests:

```bash
# Install staging app
make install-app

# Install dev app
make install-app ENV=dev

# Install prod app
make install-app ENV=prod
```

### Verify Installation

After installation, you can verify the app is installed by:
1. Opening the iOS Simulator
2. Looking for the FasterPay app icon on the home screen
3. Launching the app manually

## Troubleshooting

### Common Issues

#### 1. "App not found" Error

```
App not found: build/staging/FasterPay.app
Please build and copy your .app file to build/staging/FasterPay.app
```

**Solution**: Ensure you've copied the .app file to the correct directory with the exact name "FasterPay.app"

#### 2. "No iOS simulator running" Error

```
No iOS simulator running. Please start a simulator first.
Run 'make check-ios-simulator' to start one.
```

**Solution**: Run `make check-ios-simulator` to automatically start a simulator

#### 3. "Failed to install app" Error

**Possible causes**:
- .app file is corrupted
- Wrong architecture (device vs simulator build)
- Simulator doesn't support the app's minimum iOS version

**Solution**: 
- Rebuild the app for simulator target
- Check Xcode build logs for errors
- Ensure you're using "iOS Simulator" destination, not "iOS Device"

#### 4. App Crashes on Launch

**Possible causes**:
- Environment configuration mismatch
- Missing API keys or certificates
- Network connectivity issues

**Solution**:
- Check app logs in Xcode Console
- Verify environment settings in your app configuration
- Test network connectivity to staging/dev APIs

### Build Environment Verification

To verify your app build is correct:

```bash
# Check app bundle structure
file build/staging/FasterPay.app/FasterPay

# Should show: Mach-O 64-bit executable x86_64
# For Apple Silicon Macs, may also show: arm64
```

### Cleaning and Rebuilding

If you encounter persistent issues:

```bash
# Clean Maestro build directory
make clean-build

# Clean Xcode build (in your iOS project)
xcodebuild clean -scheme FasterPay-Staging

# Rebuild everything
xcodebuild -scheme FasterPay-Staging -destination "generic/platform=iOS Simulator" -derivedDataPath ./build

# Copy fresh build
cp -R ./build/Build/Products/Debug-iphonesimulator/FasterPay.app /path/to/maestro/build/staging/
```

## Advanced Usage

### Multiple App Versions

You can maintain multiple versions by adding version suffixes:

```
build/staging/
├── FasterPay.app              # Current version (used by tests)  
├── FasterPay-v2.1.0.app      # Version 2.1.0 backup
└── FasterPay-v2.0.9.app      # Version 2.0.9 backup
```

### Automated Build Integration

For CI/CD integration, consider adding a build script:

```bash
#!/bin/bash
# build-for-maestro.sh

ENV=${1:-staging}
PROJECT_DIR="$HOME/fasterpay-ios"
MAESTRO_DIR="$HOME/maestro"

cd "$PROJECT_DIR"
xcodebuild -scheme "FasterPay-${ENV^}" -destination "generic/platform=iOS Simulator" -derivedDataPath ./build

cp -R ./build/Build/Products/Debug-iphonesimulator/FasterPay.app "$MAESTRO_DIR/build/$ENV/"

echo "✓ Built and installed FasterPay app for $ENV environment"
```

## Getting Help

- Check `maestro/build/README.md` for quick reference
- Review Xcode build logs for compilation errors  
- Use `make help` to see all available commands
- Contact the QA team for environment-specific configuration questions