#!/usr/bin/env python3
"""
Installation script for Appium test dependencies
"""

import subprocess
import sys
import os
import platform


def run_command(command, description="Running command"):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Success")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")


def check_node_npm():
    """Check if Node.js and npm are installed"""
    print("\n📦 Checking Node.js and npm...")
    
    # Check Node.js
    if not run_command("node --version", "Checking Node.js"):
        print("❌ Node.js is not installed. Please install Node.js first.")
        print("Download from: https://nodejs.org/")
        return False
    
    # Check npm
    if not run_command("npm --version", "Checking npm"):
        print("❌ npm is not installed. Please install npm first.")
        return False
    
    return True


def install_appium_server():
    """Install Appium server globally"""
    print("\n📱 Installing Appium server...")
    
    commands = [
        "npm install -g appium",
        "npm install -g @appium/doctor"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Running: {cmd}"):
            return False
    
    return True


def install_appium_drivers():
    """Install Appium drivers"""
    print("\n🔧 Installing Appium drivers...")
    
    drivers = [
        "appium driver install xcuitest",  # iOS
        "appium driver install uiautomator2"  # Android
    ]
    
    for driver in drivers:
        run_command(driver, f"Installing: {driver}")
    
    return True


def create_virtual_environment():
    """Create Python virtual environment"""
    venv_path = os.path.join(os.path.dirname(__file__), '..', 'venv')
    
    print(f"\n🐍 Creating virtual environment at {venv_path}...")
    
    if not run_command(f"python3 -m venv {venv_path}", "Creating virtual environment"):
        return False
    
    print(f"✅ Virtual environment created at: {venv_path}")
    print(f"📝 To activate: source {venv_path}/bin/activate (Linux/Mac) or {venv_path}\\Scripts\\activate (Windows)")
    
    return True


def install_python_dependencies():
    """Install Python dependencies"""
    requirements_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    venv_path = os.path.join(os.path.dirname(__file__), '..', 'venv')
    
    print(f"\n📦 Installing Python dependencies from {requirements_path}...")
    
    if not os.path.exists(requirements_path):
        print("❌ requirements.txt not found")
        return False
    
    # Use the virtual environment's pip directly
    if platform.system() == "Windows":
        venv_pip = os.path.join(venv_path, "Scripts", "pip")
    else:
        venv_pip = os.path.join(venv_path, "bin", "pip")
    
    if not os.path.exists(venv_pip):
        print("❌ Virtual environment pip not found. Trying to use venv python -m pip...")
        if platform.system() == "Windows":
            venv_python = os.path.join(venv_path, "Scripts", "python")
        else:
            venv_python = os.path.join(venv_path, "bin", "python")
        
        return run_command(f'"{venv_python}" -m pip install -r "{requirements_path}"', "Installing Python packages")
    
    return run_command(f'"{venv_pip}" install -r "{requirements_path}"', "Installing Python packages")


def check_platform_tools():
    """Check platform-specific tools"""
    system = platform.system()
    
    print(f"\n🔍 Checking platform tools for {system}...")
    
    if system == "Darwin":  # macOS
        print("Checking iOS development tools...")
        run_command("xcode-select --version", "Checking Xcode Command Line Tools")
        run_command("xcrun --version", "Checking xcrun")
        
    # Android tools (all platforms)
    print("Checking Android development tools...")
    android_checks = [
        ("adb --version", "Android Debug Bridge (ADB)"),
        ("emulator -version", "Android Emulator")
    ]
    
    for cmd, desc in android_checks:
        run_command(cmd, f"Checking {desc}")


def run_appium_doctor():
    """Run appium-doctor to check setup"""
    print("\n🏥 Running Appium Doctor to check setup...")
    
    # Check iOS
    print("Checking iOS setup...")
    run_command("appium-doctor --ios", "Appium Doctor - iOS")
    
    # Check Android
    print("Checking Android setup...")
    run_command("appium-doctor --android", "Appium Doctor - Android")


def main():
    """Main installation process"""
    print("🚀 FasterPay Appium Test Setup")
    print("=" * 50)
    
    # Step 1: Check Python version
    print("\n1. Checking Python version...")
    check_python_version()
    
    # Step 2: Check Node.js and npm
    print("\n2. Checking Node.js and npm...")
    if not check_node_npm():
        print("\n❌ Setup failed. Please install Node.js and npm first.")
        sys.exit(1)
    
    # Step 3: Create virtual environment
    print("\n3. Setting up Python virtual environment...")
    if not create_virtual_environment():
        print("\n⚠️ Virtual environment creation failed. Continuing...")
    
    # Step 4: Install Python dependencies
    print("\n4. Installing Python dependencies...")
    if not install_python_dependencies():
        print("\n❌ Python dependencies installation failed.")
        print("💡 Make sure you're in the virtual environment if you created one.")
    
    # Step 5: Install Appium server
    print("\n5. Installing Appium server...")
    if not install_appium_server():
        print("\n❌ Appium server installation failed.")
        sys.exit(1)
    
    # Step 6: Install Appium drivers
    print("\n6. Installing Appium drivers...")
    install_appium_drivers()
    
    # Step 7: Check platform tools
    print("\n7. Checking platform tools...")
    check_platform_tools()
    
    # Step 8: Run Appium Doctor
    print("\n8. Running Appium Doctor...")
    run_appium_doctor()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. If using virtual environment, activate it:")
    print("   source venv/bin/activate (Linux/Mac)")
    print("   venv\\Scripts\\activate (Windows)")
    print("2. Start Appium server: appium")
    print("3. Place your app files in apps/ios/ and apps/android/")
    print("4. Run tests: pytest tests/")
    print("\nFor detailed instructions, see docs/SETUP.md")


if __name__ == "__main__":
    main()