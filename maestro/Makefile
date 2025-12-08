# Maestro Test Automation Makefile
# Provides common commands for platform-specific testing

# Default environment
ENV ?= staging

# Color codes for output
YELLOW = \033[1;33m
GREEN = \033[1;32m
RED = \033[1;31m
NC = \033[0m # No Color

.PHONY: help setup test-smoke-mobile test-smoke-android test-regression-mobile test-ios test-android test-cross clean

# Default target
help:
	@echo "$(YELLOW)Maestro Test Automation Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup:$(NC)"
	@echo "  make setup              - Setup test environment"
	@echo ""
	@echo "$(GREEN)Quality Gates:$(NC)"
	@echo "  make test-smoke-ios     - Run iOS-specific smoke tests"
	@echo "  make test-smoke-android - Run Android-specific smoke tests"
	@echo "  make test-regression-mobile - Run daily regression suite for both platforms"
	@echo ""
	@echo "$(GREEN)Platform Tests:$(NC)"
	@echo "  make test-ios SUITES=\"auth-ios\" - Run iOS test suites"
	@echo "  make test-android SUITES=\"auth-android\" - Run Android test suites"
	@echo ""
	@echo "$(GREEN)Utility:$(NC)"
	@echo "  make clean              - Clean reports and screenshots"
	@echo "  make clean-build        - Remove all .app files from build directory"
	@echo "  make validate-tags      - Validate test tags"
	@echo "  make check-ios-simulator - Check and start iOS simulator if needed"
	@echo "  make install-app        - Install app for current environment to simulator"
	@echo ""
	@echo "$(GREEN)Environment:$(NC)"
	@echo "  ENV=dev|staging|prod    - Set environment (default: staging)"

setup:
	@echo "$(YELLOW)Setting up test environment...$(NC)"
	@mkdir -p reports screenshots
	@echo "$(GREEN)Setup complete!$(NC)"

# Quality Gates
test-smoke-android:
	@echo "$(YELLOW)Running Android smoke tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV) PLATFORM=android); \
	echo "$(YELLOW)Using environment variables: $$ENV_VARS$(NC)"; \
	maestro test flows/quality-gates/smoke-suite-android.yaml \
		$$ENV_VARS \
		--format junit \
		--output reports/smoke-android-$(ENV)

test-smoke-ios: check-ios-simulator install-app
	@echo "$(YELLOW)Running iOS smoke tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV) PLATFORM=ios); \
	echo "$(YELLOW)Using environment variables: $$ENV_VARS$(NC)"; \
	maestro test flows/quality-gates/smoke-suite-ios.yaml \
		$$ENV_VARS \
		--format junit \
		--output reports/smoke-ios-$(ENV)

test-regression-mobile:
	@echo "$(YELLOW)Running daily regression suite for both iOS and Android on $(ENV)...$(NC)"
	@ENV_VARS_IOS=$$($(MAKE) -s extract-env-vars ENV=$(ENV) PLATFORM=ios); \
	ENV_VARS_ANDROID=$$($(MAKE) -s extract-env-vars ENV=$(ENV) PLATFORM=android); \
	echo "$(YELLOW)Running iOS regression tests...$(NC)"; \
	maestro test flows/quality-gates/daily-regression.yaml \
		$$ENV_VARS_IOS \
		--include-tags="platform:ios" \
		--format junit \
		--output reports/regression-ios-$(ENV); \
	echo "$(YELLOW)Running Android regression tests...$(NC)"; \
	maestro test flows/quality-gates/daily-regression.yaml \
		$$ENV_VARS_ANDROID \
		--include-tags="platform:android" \
		--format junit \
		--output reports/regression-android-$(ENV)


# Platform-Specific Tests
test-ios: check-ios-simulator install-app
	@echo "$(YELLOW)Running iOS test suites on $(ENV)...$(NC)"
	@if [ -z "$(SUITES)" ]; then \
		echo "$(RED)Error: SUITES parameter required.$(NC)"; \
		echo "$(YELLOW)Usage examples:$(NC)"; \
		echo "  make test-ios SUITES=\"auth-ios\""; \
		echo "  make test-ios SUITES=\"auth-ios,payment-ios\""; \
		echo "$(YELLOW)Available test suites:$(NC)"; \
		ls flows/test-suites/*ios*.yaml 2>/dev/null | sed 's/flows\/test-suites\///g; s/\.yaml//g' | sed 's/^/  - /' || echo "  No iOS test suites found"; \
		exit 1; \
	fi; \
	ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV) PLATFORM=ios); \
	echo "$(YELLOW)Environment variables: $$ENV_VARS$(NC)"; \
	SUITE_FILES=""; \
	IFS=','; \
	for suite in $(SUITES); do \
		SUITE_FILE="flows/test-suites/$$suite.yaml"; \
		if [ -f "$$SUITE_FILE" ]; then \
			if [ -z "$$SUITE_FILES" ]; then \
				SUITE_FILES="$$SUITE_FILE"; \
			else \
				SUITE_FILES="$$SUITE_FILES $$SUITE_FILE"; \
			fi; \
			echo "$(YELLOW)Adding test suite: $$SUITE_FILE$(NC)"; \
		else \
			echo "$(RED)Test suite not found: $$SUITE_FILE$(NC)"; \
			exit 1; \
		fi; \
	done; \
	echo "$(YELLOW)Running test suites: $$SUITE_FILES$(NC)"; \
	maestro test $$SUITE_FILES \
		$$ENV_VARS \
		--format junit \
		--output reports/ios-$(ENV)

test-android:
	@echo "$(YELLOW)Running Android test suites on $(ENV)...$(NC)"
	@if [ -z "$(SUITES)" ]; then \
		echo "$(RED)Error: SUITES parameter required.$(NC)"; \
		echo "$(YELLOW)Usage examples:$(NC)"; \
		echo "  make test-android SUITES=\"auth-android\""; \
		echo "  make test-android SUITES=\"auth-android,payment-android\""; \
		echo "$(YELLOW)Available test suites:$(NC)"; \
		ls flows/test-suites/*android*.yaml 2>/dev/null | sed 's/flows\/test-suites\///g; s/\.yaml//g' | sed 's/^/  - /' || echo "  No Android test suites found"; \
		exit 1; \
	fi; \
	ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV) PLATFORM=android); \
	echo "$(YELLOW)Environment variables: $$ENV_VARS$(NC)"; \
	SUITE_FILES=""; \
	IFS=','; \
	for suite in $(SUITES); do \
		SUITE_FILE="flows/test-suites/$$suite.yaml"; \
		if [ -f "$$SUITE_FILE" ]; then \
			if [ -z "$$SUITE_FILES" ]; then \
				SUITE_FILES="$$SUITE_FILE"; \
			else \
				SUITE_FILES="$$SUITE_FILES $$SUITE_FILE"; \
			fi; \
			echo "$(YELLOW)Adding test suite: $$SUITE_FILE$(NC)"; \
		else \
			echo "$(RED)Test suite not found: $$SUITE_FILE$(NC)"; \
			exit 1; \
		fi; \
	done; \
	echo "$(YELLOW)Running test suites: $$SUITE_FILES$(NC)"; \
	maestro test $$SUITE_FILES \
		$$ENV_VARS \
		--format junit \
		--output reports/android-$(ENV)

# Utility commands
clean:
	@echo "$(YELLOW)Cleaning reports and screenshots...$(NC)"
	@rm -rf reports/* screenshots/*
	@echo "$(GREEN)Clean complete!$(NC)"

clean-build:
	@echo "$(YELLOW)Cleaning build directory...$(NC)"
	@rm -rf build/*/*.app
	@echo "$(GREEN)Build clean complete!$(NC)"

validate-tags:
	@echo "$(YELLOW)Validating test tags...$(NC)"
	@if command -v python3 > /dev/null; then \
		python3 scripts/validate-tags.py; \
	else \
		echo "$(RED)Python3 not found. Skipping tag validation.$(NC)"; \
	fi

# Development helpers
dev-smoke:
	@echo "$(YELLOW)Running smoke tests in development mode...$(NC)"
	@make test-smoke-mobile ENV=dev

staging-smoke:
	@echo "$(YELLOW)Running smoke tests in staging mode...$(NC)"
	@make test-smoke-mobile ENV=staging

prod-smoke:
	@echo "$(YELLOW)Running smoke tests in production mode...$(NC)"
	@make test-smoke-mobile ENV=prod

# Quick test commands
quick-auth:
	@echo "$(YELLOW)Running quick auth validation...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV) PLATFORM=ios); \
	maestro test flows/features/auth/happy-path/sign-up-flow.yaml \
		$$ENV_VARS

quick-ios: check-ios-simulator install-app
	@echo "$(YELLOW)Running quick iOS validation...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV) PLATFORM=ios); \
	maestro test flows/features/auth/happy-path/sign-in-ios.yaml \
		$$ENV_VARS

# iOS Simulator Management
check-ios-simulator:
	@echo "$(YELLOW)Checking iOS simulator status...$(NC)"
	@echo ""
	@echo "$(YELLOW)Available compatible iOS simulators:$(NC)"
	@xcrun simctl list devices available | grep -E "(iPhone 16|iPhone 15 Pro|iPhone 14 Pro Max)" | grep "(Shutdown)" || echo "  No compatible simulators available"
	@echo ""
	@RUNNING_SIM=$$(xcrun simctl list devices | grep "Booted" | head -1); \
	PRIORITY_SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 16" | head -1); \
	if [ -z "$$PRIORITY_SIM_LINE" ]; then \
		PRIORITY_SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 15 Pro" | head -1); \
	fi; \
	if [ -z "$$PRIORITY_SIM_LINE" ]; then \
		PRIORITY_SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 14 Pro Max" | head -1); \
	fi; \
	PRIORITY_SIM_NAME=$$(echo "$$PRIORITY_SIM_LINE" | sed 's/^[[:space:]]*\([^(]*\).*/\1/' | sed 's/[[:space:]]*$$//'); \
	echo "$(YELLOW)Highest priority device: $$PRIORITY_SIM_NAME$(NC)"; \
	echo ""; \
	if [ -z "$$RUNNING_SIM" ]; then \
		echo "$(YELLOW)No iOS simulator currently running.$(NC)"; \
		echo "$(YELLOW)Starting highest priority simulator...$(NC)"; \
		SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 16" | grep "(Shutdown)" | head -1); \
		if [ -z "$$SIM_LINE" ]; then \
			SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 15 Pro" | grep "(Shutdown)" | head -1); \
		fi; \
		if [ -z "$$SIM_LINE" ]; then \
			SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 14 Pro Max" | grep "(Shutdown)" | head -1); \
		fi; \
		SIM_ID=$$(echo "$$SIM_LINE" | sed 's/.*(\([A-Z0-9-]*\)).*/\1/'); \
		SIM_NAME=$$(echo "$$SIM_LINE" | sed 's/^[[:space:]]*\([^(]*\).*/\1/' | sed 's/[[:space:]]*$$//'); \
		if [ -n "$$SIM_ID" ]; then \
			echo "$(GREEN)Selected simulator: $$SIM_NAME ($$SIM_ID)$(NC)"; \
			xcrun simctl boot "$$SIM_ID" || (echo "$(RED)Failed to start simulator$(NC)" && exit 1); \
			echo "$(YELLOW)Waiting for simulator to be ready...$(NC)"; \
			sleep 10; \
			TIMEOUT=60; \
			while [ $$TIMEOUT -gt 0 ]; do \
				if xcrun simctl list devices | grep "$$SIM_ID" | grep -q "Booted"; then \
					echo "$(GREEN)✓ Simulator '$$SIM_NAME' is ready and booted!$(NC)"; \
					break; \
				fi; \
				sleep 2; \
				TIMEOUT=$$((TIMEOUT-2)); \
			done; \
			if [ $$TIMEOUT -le 0 ]; then \
				echo "$(RED)Simulator failed to boot within timeout$(NC)"; \
				exit 1; \
			fi; \
		else \
			echo "$(RED)No compatible iOS simulator found$(NC)"; \
			exit 1; \
		fi; \
	else \
		RUNNING_NAME=$$(echo "$$RUNNING_SIM" | sed 's/^[[:space:]]*\([^(]*\).*/\1/' | sed 's/[[:space:]]*$$//'); \
		RUNNING_ID=$$(echo "$$RUNNING_SIM" | sed 's/.*(\([A-Z0-9-]*\)).*/\1/'); \
		echo "$(YELLOW)Currently running: $$RUNNING_NAME ($$RUNNING_ID)$(NC)"; \
		if echo "$$RUNNING_NAME" | grep -q "$$PRIORITY_SIM_NAME"; then \
			echo "$(GREEN)✓ Running simulator matches highest priority device!$(NC)"; \
		else \
			echo "$(YELLOW)Running simulator is not the highest priority device.$(NC)"; \
			echo "$(YELLOW)Switching to highest priority simulator...$(NC)"; \
			echo "$(YELLOW)Shutting down current simulator...$(NC)"; \
			xcrun simctl shutdown "$$RUNNING_ID"; \
			sleep 3; \
			SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 16" | grep "(Shutdown)" | head -1); \
			if [ -z "$$SIM_LINE" ]; then \
				SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 15 Pro" | grep "(Shutdown)" | head -1); \
			fi; \
			if [ -z "$$SIM_LINE" ]; then \
				SIM_LINE=$$(xcrun simctl list devices available | grep "iPhone 14 Pro Max" | grep "(Shutdown)" | head -1); \
			fi; \
			SIM_ID=$$(echo "$$SIM_LINE" | sed 's/.*(\([A-Z0-9-]*\)).*/\1/'); \
			SIM_NAME=$$(echo "$$SIM_LINE" | sed 's/^[[:space:]]*\([^(]*\).*/\1/' | sed 's/[[:space:]]*$$//'); \
			if [ -n "$$SIM_ID" ]; then \
				echo "$(GREEN)Starting priority simulator: $$SIM_NAME ($$SIM_ID)$(NC)"; \
				xcrun simctl boot "$$SIM_ID" || (echo "$(RED)Failed to start simulator$(NC)" && exit 1); \
				echo "$(YELLOW)Waiting for simulator to be ready...$(NC)"; \
				sleep 10; \
				TIMEOUT=60; \
				while [ $$TIMEOUT -gt 0 ]; do \
					if xcrun simctl list devices | grep "$$SIM_ID" | grep -q "Booted"; then \
						echo "$(GREEN)✓ Priority simulator '$$SIM_NAME' is ready and booted!$(NC)"; \
						break; \
					fi; \
					sleep 2; \
					TIMEOUT=$$((TIMEOUT-2)); \
				done; \
				if [ $$TIMEOUT -le 0 ]; then \
					echo "$(RED)Simulator failed to boot within timeout$(NC)"; \
					exit 1; \
				fi; \
			else \
				echo "$(RED)No compatible iOS simulator found$(NC)"; \
				exit 1; \
			fi; \
		fi; \
	fi
	@echo ""

# App Installation Management
install-app:
	@echo "$(YELLOW)Installing app for $(ENV) environment...$(NC)"
	@RUNNING_SIM=$$(xcrun simctl list devices | grep "Booted" | head -1); \
	if [ -z "$$RUNNING_SIM" ]; then \
		echo "$(RED)No iOS simulator running. Please start a simulator first.$(NC)"; \
		echo "$(YELLOW)Run 'make check-ios-simulator' to start one.$(NC)"; \
		exit 1; \
	fi; \
	SIM_ID=$$(echo "$$RUNNING_SIM" | sed 's/.*(\([A-Z0-9-]*\)).*/\1/'); \
	SIM_NAME=$$(echo "$$RUNNING_SIM" | sed 's/^[[:space:]]*\([^(]*\).*/\1/' | sed 's/[[:space:]]*$$//'); \
	echo "$(GREEN)Target simulator: $$SIM_NAME ($$SIM_ID)$(NC)"; \
	APP_PATH="build/$(ENV)/FasterPay.app"; \
	if [ ! -d "$$APP_PATH" ]; then \
		echo "$(RED)App not found: $$APP_PATH$(NC)"; \
		echo "$(YELLOW)Please build and copy your .app file to $$APP_PATH$(NC)"; \
		echo "$(YELLOW)See docs/APP_BUILD_GUIDE.md for instructions.$(NC)"; \
		exit 1; \
	fi; \
	echo "$(YELLOW)Installing app from: $$APP_PATH$(NC)"; \
	xcrun simctl install "$$SIM_ID" "$$APP_PATH" || (echo "$(RED)Failed to install app$(NC)" && exit 1); \
	echo "$(GREEN)✓ App successfully installed on $$SIM_NAME$(NC)"

# Helper function to extract environment variables from YAML config
extract-env-vars:
	@if [ -n "$(PLATFORM)" ]; then \
		CONFIG_FILE="configs/env-$(ENV)-$(PLATFORM).yaml"; \
	else \
		CONFIG_FILE="configs/env-$(ENV).yaml"; \
	fi; \
	if [ ! -f "$$CONFIG_FILE" ]; then \
		echo "$(RED)Config file not found: $$CONFIG_FILE$(NC)"; \
		echo "$(YELLOW)Available config files:$(NC)"; \
		ls configs/env-*.yaml 2>/dev/null || echo "  No config files found"; \
		exit 1; \
	fi; \
	grep -A 20 "^env:" "$$CONFIG_FILE" | grep "^  [A-Z_]" | sed 's/^  /-e /;s/: */=/;s/"//g' | tr '\n' ' '