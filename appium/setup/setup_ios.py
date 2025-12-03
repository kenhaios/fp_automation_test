#!/usr/bin/env python3
"""
iOS-specific setup script for Appium testing
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


def check_macos():
    """Check if running on macOS"""
    if platform.system() != "Darwin":
        print("❌ iOS development requires macOS")
        sys.exit(1)
    print("✅ macOS detected")


def check_xcode():
    """Check Xcode installation"""
    print("\n🔍 Checking Xcode installation...")
    
    # Check if Xcode is installed
    result = run_command("xcode-select --print-path", "Checking Xcode path", check=False)
    if not result or result.returncode != 0:
        print("❌ Xcode Command Line Tools not found")
        print("📝 Install with: xcode-select --install")
        return False
    
    # Check Xcode version
    run_command("xcodebuild -version", "Checking Xcode version", check=False)
    
    return True


def check_ios_simulators():
    """Check available iOS simulators"""
    print("\n📱 Checking iOS Simulators...")
    
    result = run_command("xcrun simctl list devices available", 
                        "Listing available simulators", check=False)
    
    if result and result.returncode == 0:
        output = result.stdout
        ios_simulators = []
        current_ios = None
        
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('-- iOS'):
                current_ios = line.replace('-- iOS ', '').replace(' --', '')
            elif current_ios and line and '(' in line and ')' in line:
                sim_name = line.split('(')[0].strip()
                sim_id = line.split('(')[1].split(')')[0]
                ios_simulators.append({
                    'name': sim_name,
                    'id': sim_id,
                    'ios_version': current_ios
                })
        
        if ios_simulators:
            print(f"✅ Found {len(ios_simulators)} iOS simulators")
            print("\nAvailable simulators:")
            for sim in ios_simulators[:5]:  # Show first 5
                print(f"  - {sim['name']} (iOS {sim['ios_version']})")
            
            return ios_simulators
        else:
            print("⚠️ No iOS simulators found")
            return []
    
    print("❌ Failed to list simulators")
    return []


def install_ios_dependencies():
    """Install iOS-specific dependencies"""
    print("\n📦 Installing iOS dependencies...")
    
    # Install libimobiledevice for real device support
    homebrew_packages = [
        "libimobiledevice",
        "ideviceinstaller",
        "carthage",  # Dependency manager
        "ios-webkit-debug-proxy"  # For Safari debugging
    ]
    
    # Check if Homebrew is installed
    brew_check = run_command("brew --version", "Checking Homebrew", check=False)
    if not brew_check or brew_check.returncode != 0:
        print("⚠️ Homebrew not found. Installing Homebrew...")
        install_brew = run_command('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                                 "Installing Homebrew", check=False)
        if not install_brew or install_brew.returncode != 0:
            print("❌ Failed to install Homebrew")
            return False
    
    # Install packages
    for package in homebrew_packages:
        run_command(f"brew install {package}", f"Installing {package}", check=False)
    
    return True


def setup_webdriveragent():
    """Setup WebDriverAgent for iOS testing"""
    print("\n🔧 Setting up WebDriverAgent...")
    
    # Check if WebDriverAgent is already set up
    wda_check = run_command("find /usr/local/lib/node_modules/appium -name 'WebDriverAgent.xcodeproj' 2>/dev/null",
                           "Checking WebDriverAgent", check=False)
    
    if wda_check and wda_check.stdout.strip():
        wda_path = wda_check.stdout.strip()
        print(f"✅ WebDriverAgent found at: {wda_path}")
        
        print("\n📝 WebDriverAgent Setup Instructions:")
        print("1. Open WebDriverAgent.xcodeproj in Xcode")
        print(f"   Path: {wda_path}")
        print("2. Select 'WebDriverAgentLib' target")
        print("3. In 'Signing & Capabilities', select your Development Team")
        print("4. Change Bundle Identifier to something unique (e.g., com.yourname.WebDriverAgentLib)")
        print("5. Repeat for 'WebDriverAgentRunner' target")
        print("6. Build the project (Cmd+B)")
        
        return True
    else:
        print("❌ WebDriverAgent not found")
        print("💡 Make sure Appium is installed with XCUITest driver")
        return False


def check_connected_devices():
    """Check connected iOS devices"""
    print("\n📱 Checking connected iOS devices...")
    
    # Check for connected devices
    result = run_command("idevice_id -l", "Listing connected iOS devices", check=False)
    
    if result and result.returncode == 0:
        devices = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        if devices:
            print(f"✅ Found {len(devices)} connected iOS device(s):")
            for device_id in devices:
                # Get device name
                name_result = run_command(f"ideviceinfo -u {device_id} -k DeviceName",
                                        f"Getting device name for {device_id}", check=False)
                device_name = name_result.stdout.strip() if name_result and name_result.returncode == 0 else "Unknown"
                
                # Get iOS version
                version_result = run_command(f"ideviceinfo -u {device_id} -k ProductVersion",
                                           f"Getting iOS version for {device_id}", check=False)
                ios_version = version_result.stdout.strip() if version_result and version_result.returncode == 0 else "Unknown"
                
                print(f"  - {device_name} (UDID: {device_id}, iOS: {ios_version})")
        else:
            print("⚠️ No iOS devices connected")
        
        return devices
    else:
        print("⚠️ Unable to check connected devices (libimobiledevice may not be installed)")
        return []


def create_ios_test_config():
    """Create iOS test configuration file"""
    print("\n📝 Creating iOS test configuration...")
    
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    config_file = os.path.join(config_dir, 'ios_test_config.json')
    
    # Get available simulators
    simulators = check_ios_simulators()
    devices = check_connected_devices()
    
    config = {
        "available_simulators": simulators[:3] if simulators else [],  # Top 3
        "connected_devices": devices,
        "default_simulator": simulators[0] if simulators else None,
        "webdriveragent_path": "",
        "team_id": "YOUR_TEAM_ID_HERE",
        "setup_date": subprocess.check_output(["date"], text=True).strip()
    }
    
    try:
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration saved to: {config_file}")
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")


def main():
    """Main iOS setup process"""
    print("🍎 iOS Appium Setup")
    print("=" * 40)
    
    # Check if running on macOS
    print("\n1. Checking macOS...")
    check_macos()
    
    # Check Xcode
    print("\n2. Checking Xcode...")
    if not check_xcode():
        print("\n❌ Xcode setup required. Please install Xcode and run again.")
        sys.exit(1)
    
    # Check iOS simulators
    print("\n3. Checking iOS Simulators...")
    simulators = check_ios_simulators()
    
    # Install iOS dependencies
    print("\n4. Installing iOS dependencies...")
    install_ios_dependencies()
    
    # Setup WebDriverAgent
    print("\n5. Checking WebDriverAgent...")
    setup_webdriveragent()
    
    # Check connected devices
    print("\n6. Checking connected devices...")
    devices = check_connected_devices()
    
    # Create configuration
    print("\n7. Creating test configuration...")
    create_ios_test_config()
    
    print("\n" + "=" * 40)
    print("🎉 iOS setup complete!")
    print("\nNext steps for iOS testing:")
    print("1. Place your iOS app (.app file) in apps/ios/")
    print("2. For real device testing:")
    print("   - Update config/ios_device.py with your Team ID")
    print("   - Trust the developer certificate on your device")
    print("   - Configure WebDriverAgent in Xcode")
    print("3. Start Appium: appium")
    print("4. Run iOS tests: pytest tests/ios/ --platform=ios_simulator")
    print("\nFor troubleshooting, see docs/DEVICE_SETUP.md")


if __name__ == "__main__":
    main()