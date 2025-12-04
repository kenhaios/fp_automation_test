"""pytest configuration and fixtures"""

import pytest


def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        "--platform", 
        action="store", 
        default="ios_simulator",
        help="Platform to run tests on: ios_simulator, ios_device, android_emulator, android_device"
    )
    parser.addoption(
        "--device-id", 
        action="store", 
        default=None,
        help="Device ID/UDID for real device testing"
    )
    parser.addoption(
        "--appium-server", 
        action="store", 
        default="http://localhost:4723",
        help="Appium server URL"
    )