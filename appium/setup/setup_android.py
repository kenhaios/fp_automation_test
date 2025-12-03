#!/usr/bin/env python3
"""
Android-specific setup script for Appium testing
"""

import subprocess
import sys
import os
import json
import platform


def run_command(command, description="Running command", check=True):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print("⚠️ Warning" if not check else "❌ Failed")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print("❌ Failed")
        print(f"Error: {e.stderr}")
        return None


def check_android_sdk():
    """Check Android SDK installation"""
    print("\n🔍 Checking Android SDK...")
    
    # Check ANDROID_HOME
    android_home = os.environ.get('ANDROID_HOME')
    if not android_home:
        android_home = os.environ.get('ANDROID_SDK_ROOT')
    
    if not android_home:
        print("❌ ANDROID_HOME or ANDROID_SDK_ROOT not set")
        print("📝 Please set ANDROID_HOME environment variable")
        print("   Example: export ANDROID_HOME=/path/to/android-sdk")
        return False
    
    print(f"✅ Android SDK found at: {android_home}")
    
    # Check if SDK directory exists
    if not os.path.exists(android_home):
        print(f"❌ Android SDK directory does not exist: {android_home}")
        return False
    
    return True


def check_android_tools():
    """Check Android development tools"""
    print("\n🔧 Checking Android tools...")
    
    tools = [
        ("adb", "Android Debug Bridge"),
        ("emulator", "Android Emulator"),
        ("avdmanager", "AVD Manager")
    ]
    
    results = {}
    for tool, description in tools:
        result = run_command(f"{tool} --version", f"Checking {description}", check=False)
        results[tool] = result and result.returncode == 0
    
    return results


def check_connected_devices():
    """Check connected Android devices"""
    print("\n📱 Checking connected Android devices...")
    
    result = run_command("adb devices", "Listing connected devices", check=False)
    
    devices = []
    if result and result.returncode == 0:
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        for line in lines:
            line = line.strip()
            if line and '\t' in line:
                device_id, status = line.split('\t')
                if status == 'device':
                    devices.append(device_id)
        
        if devices:
            print(f"✅ Found {len(devices)} connected Android device(s):")
            for device_id in devices:
                # Get device model
                model_result = run_command(f"adb -s {device_id} shell getprop ro.product.model",
                                         f"Getting model for {device_id}", check=False)
                model = model_result.stdout.strip() if model_result and model_result.returncode == 0 else "Unknown"
                
                # Get Android version
                version_result = run_command(f"adb -s {device_id} shell getprop ro.build.version.release",
                                           f"Getting Android version for {device_id}", check=False)
                android_version = version_result.stdout.strip() if version_result and version_result.returncode == 0 else "Unknown"
                
                print(f"  - {model} (ID: {device_id}, Android: {android_version})")
        else:
            print("⚠️ No Android devices connected")
    else:
        print("❌ Failed to check connected devices")
    
    return devices


def check_emulators():
    """Check available Android emulators"""
    print("\n🤖 Checking Android Emulators...")
    
    result = run_command("emulator -list-avds", "Listing AVDs", check=False)
    
    avds = []
    if result and result.returncode == 0:
        avds = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        if avds:
            print(f"✅ Found {len(avds)} Android Virtual Device(s):")
            for avd in avds:
                print(f"  - {avd}")
        else:
            print("⚠️ No Android Virtual Devices found")
            print("📝 Create AVDs using Android Studio or avdmanager command")
    else:
        print("❌ Failed to list emulators")
    
    return avds


def install_android_dependencies():
    """Install Android-specific dependencies"""
    print("\n📦 Installing Android dependencies...")
    
    # For macOS, use Homebrew
    if platform.system() == "Darwin":
        run_command("brew install android-platform-tools", "Installing Android platform tools", check=False)
    
    # Check if we can install additional SDK components
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if android_home:
        sdkmanager_path = os.path.join(android_home, 'cmdline-tools', 'latest', 'bin', 'sdkmanager')
        if os.path.exists(sdkmanager_path):
            print("\n📦 Installing additional SDK components...")
            components = [
                "platform-tools",
                "build-tools;34.0.0",
                "platforms;android-34",
                "emulator",
                "system-images;android-34;google_apis;x86_64"
            ]
            
            for component in components:
                run_command(f'echo "y" | {sdkmanager_path} "{component}"',
                          f"Installing {component}", check=False)
        else:
            print("⚠️ SDK Manager not found. Install Android Studio for complete setup.")


def setup_android_environment():
    """Setup Android environment variables"""
    print("\n🔧 Setting up Android environment...")
    
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if not android_home:
        print("❌ Cannot setup environment: ANDROID_HOME not set")
        return False
    
    # Check PATH
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    platform_tools = os.path.join(android_home, 'platform-tools')
    tools = os.path.join(android_home, 'tools')
    
    missing_paths = []
    if platform_tools not in path_dirs:
        missing_paths.append(platform_tools)
    if tools not in path_dirs and os.path.exists(tools):
        missing_paths.append(tools)
    
    if missing_paths:
        print("⚠️ Some Android tools are not in PATH:")
        for path in missing_paths:
            print(f"  - {path}")
        
        print("\n📝 Add to your shell profile (.bashrc, .zshrc, etc.):")
        for path in missing_paths:
            print(f"export PATH=$PATH:{path}")
    else:
        print("✅ Android tools are in PATH")
    
    return True


def enable_developer_options():
    """Instructions for enabling developer options"""
    print("\n👨‍💻 Developer Options Setup:")
    print("For real device testing, ensure Developer Options are enabled:")
    print("1. Go to Settings → About Phone")
    print("2. Tap 'Build Number' 7 times")
    print("3. Go to Settings → Developer Options")
    print("4. Enable 'USB Debugging'")
    print("5. Enable 'Stay awake'")
    print("6. Enable 'Allow mock locations' (if needed)")


def create_android_test_config():
    """Create Android test configuration file"""
    print("\n📝 Creating Android test configuration...")
    
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    config_file = os.path.join(config_dir, 'android_test_config.json')
    
    # Get available emulators and devices
    avds = check_emulators()
    devices = check_connected_devices()
    
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT', "")
    
    config = {
        "android_home": android_home,
        "available_avds": avds,
        "connected_devices": devices,
        "default_avd": avds[0] if avds else None,
        "app_package": "com.fasterpay.ewallet",
        "app_activity": "com.fasterpay.ewallet.MainActivity",
        "setup_date": subprocess.check_output(["date"], text=True).strip()
    }
    
    try:
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration saved to: {config_file}")
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")


def test_emulator_launch():
    """Test launching an emulator"""
    print("\n🚀 Testing emulator launch...")
    
    avds = check_emulators()
    if not avds:
        print("⚠️ No emulators available to test")
        return
    
    test_avd = avds[0]
    print(f"Testing launch of: {test_avd}")
    
    # Start emulator in headless mode for quick test
    result = run_command(f"emulator -avd {test_avd} -no-window -no-audio &",
                        f"Testing emulator launch", check=False)
    
    if result:
        print("✅ Emulator launch command executed")
        print("💡 Kill with: pkill -f emulator")
    else:
        print("❌ Failed to launch emulator")


def main():
    """Main Android setup process"""
    print("🤖 Android Appium Setup")
    print("=" * 40)
    
    # Check Android SDK
    print("\n1. Checking Android SDK...")
    if not check_android_sdk():
        print("\n❌ Android SDK setup required.")
        print("Please install Android Studio or Android SDK and set ANDROID_HOME")
        sys.exit(1)
    
    # Check Android tools
    print("\n2. Checking Android tools...")
    tools_status = check_android_tools()
    
    # Install dependencies
    print("\n3. Installing Android dependencies...")
    install_android_dependencies()
    
    # Setup environment
    print("\n4. Setting up environment...")
    setup_android_environment()
    
    # Check connected devices
    print("\n5. Checking connected devices...")
    devices = check_connected_devices()
    
    # Check emulators
    print("\n6. Checking emulators...")
    avds = check_emulators()
    
    # Developer options instructions
    print("\n7. Developer options setup...")
    enable_developer_options()
    
    # Create configuration
    print("\n8. Creating test configuration...")
    create_android_test_config()
    
    # Test emulator (optional)
    if avds:
        print("\n9. Testing emulator...")
        test_emulator_launch()
    
    print("\n" + "=" * 40)
    print("🎉 Android setup complete!")
    print("\nNext steps for Android testing:")
    print("1. Place your Android app (.apk file) in apps/android/")
    print("2. For real device testing:")
    print("   - Connect device via USB")
    print("   - Enable USB debugging in Developer Options")
    print("   - Trust the computer when prompted")
    print("3. For emulator testing:")
    print("   - Create AVDs using Android Studio if none exist")
    print("4. Start Appium: appium")
    print("5. Run Android tests: pytest tests/android/ --platform=android_emulator")
    print("\nFor troubleshooting, see docs/DEVICE_SETUP.md")


if __name__ == "__main__":
    main()