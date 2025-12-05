"""Utility to generate Appium Inspector compatible capabilities"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class InspectorCapabilityGenerator:
    """Generate simplified capabilities for Appium Inspector"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / "config"
        self.apps_dir = Path(__file__).parent.parent / "apps" / "ios"
    
    def generate_simulator_caps(self, 
                              device_name: str = "iPhone 14", 
                              ios_version: str = "17.2",
                              app_name: str = "Fasterpay.app") -> Dict[str, Any]:
        """Generate iOS simulator capabilities for Inspector"""
        app_path = str(self.apps_dir / app_name)
        
        caps = {
            "platformName": "iOS",
            "appium:platformVersion": ios_version,
            "appium:deviceName": device_name,
            "appium:automationName": "XCUITest",
            "appium:app": app_path,
            "appium:bundleId": "com.fasterpay.app.staging",
            "appium:noReset": False,
            "appium:newCommandTimeout": 300
        }
        
        return caps
    
    def generate_device_caps(self, 
                           udid: str,
                           device_name: str = "iPhone", 
                           ios_version: str = "16.0",
                           app_name: str = "Fasterpay.ipa",
                           team_id: str = "37N222R38X") -> Dict[str, Any]:
        """Generate iOS device capabilities for Inspector"""
        app_path = str(self.apps_dir / app_name)
        
        caps = {
            "platformName": "iOS",
            "appium:platformVersion": ios_version,
            "appium:deviceName": device_name,
            "appium:udid": udid,
            "appium:automationName": "XCUITest",
            "appium:app": app_path,
            "appium:bundleId": "com.fasterpay.app.staging",
            "appium:noReset": False,
            "appium:newCommandTimeout": 300,
            "appium:xcodeOrgId": team_id,
            "appium:xcodeSigningId": "iPhone Developer",
            "appium:useNewWDA": True
        }
        
        return caps
    
    def generate_legacy_format_caps(self, caps: Dict[str, Any]) -> Dict[str, Any]:
        """Convert W3C capabilities to legacy format (if needed for older Inspector versions)"""
        legacy_caps = {}
        
        for key, value in caps.items():
            if key.startswith("appium:"):
                # Remove appium: prefix for legacy format
                legacy_key = key.replace("appium:", "")
                legacy_caps[legacy_key] = value
            else:
                legacy_caps[key] = value
        
        return legacy_caps
    
    def save_inspector_config(self, caps: Dict[str, Any], filename: str) -> str:
        """Save capabilities to JSON file for Inspector"""
        config_path = self.config_dir / filename
        
        with open(config_path, 'w') as f:
            json.dump(caps, f, indent=2)
        
        print(f"Inspector config saved to: {config_path}")
        return str(config_path)
    
    def get_available_simulators(self) -> Dict[str, Any]:
        """Get available simulators from config"""
        try:
            with open(self.config_dir / "ios_test_config.json", 'r') as f:
                config = json.load(f)
            return config.get("available_simulators", [])
        except FileNotFoundError:
            return []
    
    def get_connected_devices(self) -> list:
        """Get connected device UDIDs from config"""
        try:
            with open(self.config_dir / "ios_test_config.json", 'r') as f:
                config = json.load(f)
            return config.get("connected_devices", [])
        except FileNotFoundError:
            return []
    
    def generate_all_inspector_configs(self):
        """Generate all possible Inspector configurations"""
        print("Generating Appium Inspector configurations...")
        
        # Simulator configuration
        sim_caps = self.generate_simulator_caps()
        self.save_inspector_config(sim_caps, "inspector_ios_simulator.json")
        
        # Legacy simulator configuration
        sim_caps_legacy = self.generate_legacy_format_caps(sim_caps)
        self.save_inspector_config(sim_caps_legacy, "inspector_ios_simulator_legacy.json")
        
        # Device configuration (if devices are available)
        devices = self.get_connected_devices()
        if devices:
            device_caps = self.generate_device_caps(udid=devices[0])
            self.save_inspector_config(device_caps, "inspector_ios_device.json")
            
            # Legacy device configuration
            device_caps_legacy = self.generate_legacy_format_caps(device_caps)
            self.save_inspector_config(device_caps_legacy, "inspector_ios_device_legacy.json")
        
        print("\n✅ Inspector configurations generated successfully!")
        print(f"📁 Location: {self.config_dir}")
        print("\n📋 Available configurations:")
        print("  • inspector_ios_simulator.json (W3C format)")
        print("  • inspector_ios_simulator_legacy.json (Legacy format)")
        if devices:
            print("  • inspector_ios_device.json (W3C format)")
            print("  • inspector_ios_device_legacy.json (Legacy format)")
        
        return True


def main():
    """Command line interface for generating Inspector configs"""
    generator = InspectorCapabilityGenerator()
    
    print("🔧 Appium Inspector Configuration Generator")
    print("=" * 50)
    
    # Check for available devices
    simulators = generator.get_available_simulators()
    devices = generator.get_connected_devices()
    
    print(f"📱 Available simulators: {len(simulators)}")
    for sim in simulators:
        print(f"   - {sim['name']} (iOS {sim['ios_version']})")
    
    print(f"📲 Connected devices: {len(devices)}")
    for device in devices:
        print(f"   - {device}")
    
    print("\nGenerating configurations...")
    generator.generate_all_inspector_configs()
    
    print("\n🚀 Usage Instructions:")
    print("1. Open Appium Inspector")
    print("2. Set Remote Path: /")
    print("3. Set Remote Host: localhost")
    print("4. Set Remote Port: 4723")
    print("5. Copy capabilities from one of the generated JSON files")
    print("6. If you get capability errors, try the legacy format files")


if __name__ == "__main__":
    main()