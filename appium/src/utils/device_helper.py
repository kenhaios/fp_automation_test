"""Device helper utilities for Appium tests"""

import subprocess
import platform
from typing import Dict, List, Optional


class DeviceHelper:
    """Utility class for device management and information"""
    
    @staticmethod
    def get_connected_ios_devices() -> List[Dict[str, str]]:
        """
        Get list of connected iOS devices
        
        Returns:
            List of dictionaries with device information
        """
        devices = []
        try:
            # Use idevice_id to list connected devices
            result = subprocess.run(['idevice_id', '-l'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                udids = result.stdout.strip().split('\n')
                for udid in udids:
                    if udid.strip():
                        device_info = DeviceHelper._get_ios_device_info(udid.strip())
                        device_info['udid'] = udid.strip()
                        devices.append(device_info)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("idevice_id not found or timeout. Install libimobiledevice for device detection.")
        
        return devices
    
    @staticmethod
    def _get_ios_device_info(udid: str) -> Dict[str, str]:
        """
        Get iOS device information for specific UDID
        
        Args:
            udid: Device UDID
            
        Returns:
            Dictionary with device information
        """
        try:
            # Get device name
            name_result = subprocess.run(
                ['ideviceinfo', '-u', udid, '-k', 'DeviceName'], 
                capture_output=True, text=True, timeout=10
            )
            device_name = name_result.stdout.strip() if name_result.returncode == 0 else "Unknown iOS Device"
            
            # Get iOS version
            version_result = subprocess.run(
                ['ideviceinfo', '-u', udid, '-k', 'ProductVersion'], 
                capture_output=True, text=True, timeout=10
            )
            ios_version = version_result.stdout.strip() if version_result.returncode == 0 else "Unknown"
            
            return {
                'device_name': device_name,
                'ios_version': ios_version,
                'platform': 'iOS'
            }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'device_name': "Unknown iOS Device",
                'ios_version': "Unknown",
                'platform': 'iOS'
            }
    
    @staticmethod
    def get_connected_android_devices() -> List[Dict[str, str]]:
        """
        Get list of connected Android devices
        
        Returns:
            List of dictionaries with device information
        """
        devices = []
        try:
            # Use adb to list connected devices
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip() and '\tdevice' in line:
                        device_id = line.split('\t')[0]
                        device_info = DeviceHelper._get_android_device_info(device_id)
                        device_info['device_id'] = device_id
                        devices.append(device_info)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("adb not found or timeout. Ensure Android SDK is installed and adb is in PATH.")
        
        return devices
    
    @staticmethod
    def _get_android_device_info(device_id: str) -> Dict[str, str]:
        """
        Get Android device information for specific device ID
        
        Args:
            device_id: Android device ID
            
        Returns:
            Dictionary with device information
        """
        try:
            # Get device model
            model_result = subprocess.run(
                ['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.model'], 
                capture_output=True, text=True, timeout=10
            )
            device_name = model_result.stdout.strip() if model_result.returncode == 0 else "Unknown Android Device"
            
            # Get Android version
            version_result = subprocess.run(
                ['adb', '-s', device_id, 'shell', 'getprop', 'ro.build.version.release'], 
                capture_output=True, text=True, timeout=10
            )
            android_version = version_result.stdout.strip() if version_result.returncode == 0 else "Unknown"
            
            return {
                'device_name': device_name,
                'android_version': android_version,
                'platform': 'Android'
            }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'device_name': "Unknown Android Device",
                'android_version': "Unknown",
                'platform': 'Android'
            }
    
    @staticmethod
    def get_ios_simulators() -> List[Dict[str, str]]:
        """
        Get list of available iOS simulators
        
        Returns:
            List of dictionaries with simulator information
        """
        simulators = []
        try:
            result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', 'available'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                current_runtime = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('-- iOS'):
                        current_runtime = line.replace('-- iOS ', '').replace(' --', '')
                    elif line and current_runtime and '(' in line and ')' in line:
                        # Parse simulator line: "iPhone 14 (12345678-1234-1234-1234-123456789ABC) (Booted)"
                        parts = line.split('(')
                        if len(parts) >= 2:
                            sim_name = parts[0].strip()
                            sim_id = parts[1].split(')')[0]
                            simulators.append({
                                'device_name': sim_name,
                                'ios_version': current_runtime,
                                'simulator_id': sim_id,
                                'platform': 'iOS Simulator'
                            })
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("xcrun not found or timeout. Ensure Xcode is installed.")
        
        return simulators
    
    @staticmethod
    def get_android_emulators() -> List[Dict[str, str]]:
        """
        Get list of available Android emulators
        
        Returns:
            List of dictionaries with emulator information
        """
        emulators = []
        try:
            # Get list of AVDs
            result = subprocess.run(['emulator', '-list-avds'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                avd_names = [name.strip() for name in result.stdout.split('\n') if name.strip()]
                for avd_name in avd_names:
                    emulators.append({
                        'device_name': avd_name,
                        'avd_name': avd_name,
                        'platform': 'Android Emulator'
                    })
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("emulator command not found. Ensure Android SDK is installed and emulator is in PATH.")
        
        return emulators
    
    @staticmethod
    def is_appium_server_running(server_url: str = "http://localhost:4723") -> bool:
        """
        Check if Appium server is running
        
        Args:
            server_url: Appium server URL
            
        Returns:
            True if server is running, False otherwise
        """
        try:
            import requests
            response = requests.get(f"{server_url}/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """
        Get system information
        
        Returns:
            Dictionary with system information
        """
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'machine': platform.machine(),
            'python_version': platform.python_version()
        }
    
    @staticmethod
    def check_prerequisites() -> Dict[str, bool]:
        """
        Check if required tools are installed
        
        Returns:
            Dictionary with availability status of each tool
        """
        tools = {
            'adb': DeviceHelper._check_command('adb'),
            'idevice_id': DeviceHelper._check_command('idevice_id'),
            'xcrun': DeviceHelper._check_command('xcrun'),
            'emulator': DeviceHelper._check_command('emulator')
        }
        return tools
    
    @staticmethod
    def _check_command(command: str) -> bool:
        """Check if a command is available in PATH"""
        try:
            subprocess.run([command, '--version'], 
                         capture_output=True, timeout=5)
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            try:
                # Try alternative version check
                subprocess.run([command, '-version'], 
                             capture_output=True, timeout=5)
                return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                return False