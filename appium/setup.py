from setuptools import setup, find_packages

setup(
    name="fp-appium-tests",
    version="1.0.0",
    description="Appium automation tests for FasterPay E-Wallet mobile application",
    author="FasterPay QA Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "Appium-Python-Client>=3.1.0",
        "selenium>=4.15.0",
        "pytest>=7.4.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "pytest-html",
            "allure-pytest",
        ]
    },
)