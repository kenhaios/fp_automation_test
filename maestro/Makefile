# Maestro Test Automation Makefile
# Provides common commands for platform-specific testing

# Default environment
ENV ?= staging

# Color codes for output
YELLOW = \033[1;33m
GREEN = \033[1;32m
RED = \033[1;31m
NC = \033[0m # No Color

.PHONY: help setup test-smoke test-regression test-auth test-ios test-android test-all clean

# Default target
help:
	@echo "$(YELLOW)Maestro Test Automation Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup:$(NC)"
	@echo "  make setup              - Setup test environment"
	@echo ""
	@echo "$(GREEN)Quality Gates:$(NC)"
	@echo "  make test-smoke         - Run smoke test suite"
	@echo "  make test-smoke-ios     - Run iOS-specific smoke tests"
	@echo "  make test-regression    - Run daily regression suite"
	@echo ""
	@echo "$(GREEN)Feature Tests:$(NC)"
	@echo "  make test-auth          - Run all authentication tests"
	@echo "  make test-auth-happy    - Run authentication happy paths only"
	@echo ""
	@echo "$(GREEN)Platform Tests:$(NC)"
	@echo "  make test-ios           - Run all iOS tests"
	@echo "  make test-android       - Run all Android tests"
	@echo "  make test-cross         - Run cross-platform tests only"
	@echo ""
	@echo "$(GREEN)Comprehensive Tests:$(NC)"
	@echo "  make test-all-happy     - Run all happy path tests"
	@echo "  make test-all           - Run all tests"
	@echo ""
	@echo "$(GREEN)Custom Tag Tests:$(NC)"
	@echo "  make test-by-tag INCLUDE_TAGS=\"tag1,tag2\" - Run tests with specific tags"
	@echo "  make test-by-tag EXCLUDE_TAGS=\"tag3\"      - Exclude tests with specific tags"
	@echo "  make test-p0            - Run P0 priority tests"
	@echo "  make test-p1            - Run P1 priority tests"
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
test-smoke:
	@echo "$(YELLOW)Running smoke test suite on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/quality-gates/smoke-suite.yaml \
		$$ENV_VARS \
		--format junit \
		--output reports/smoke-$(ENV)

test-smoke-ios: check-ios-simulator install-app
	@echo "$(YELLOW)Running iOS smoke tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	echo "$(YELLOW)Using environment variables: $$ENV_VARS$(NC)"; \
	maestro test flows/quality-gates/smoke-suite-ios.yaml \
		$$ENV_VARS \
		--format junit \
		--output reports/smoke-ios-$(ENV)

test-regression:
	@echo "$(YELLOW)Running daily regression suite on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/quality-gates/daily-regression.yaml \
		$$ENV_VARS \
		--format junit \
		--output reports/regression-$(ENV)

# Feature Tests
test-auth:
	@echo "$(YELLOW)Running all authentication tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/test-suites/auth-all.yaml \
		$$ENV_VARS \
		--format junit \
		--output reports/auth-all-$(ENV)

test-auth-happy:
	@echo "$(YELLOW)Running authentication happy path tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/ \
		$$ENV_VARS \
		--format junit \
		--output reports/auth-happy-$(ENV)

# Platform-Specific Tests
test-ios: check-ios-simulator install-app
	@echo "$(YELLOW)Running all iOS tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/ flows/features/auth/negative/ flows/features/auth/edge-cases/ \
		--include-tags="platform:ios" \
		$$ENV_VARS \
		--format junit \
		--output reports/ios-all-$(ENV)

test-android:
	@echo "$(YELLOW)Running all Android tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/ flows/features/auth/negative/ flows/features/auth/edge-cases/ \
		--include-tags="platform:android" \
		$$ENV_VARS \
		--format junit \
		--output reports/android-all-$(ENV)

test-cross:
	@echo "$(YELLOW)Running cross-platform tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/ flows/features/auth/negative/ flows/features/auth/edge-cases/ \
		--include-tags="platform:ios,platform:android" \
		$$ENV_VARS \
		--format junit \
		--output reports/cross-platform-$(ENV)

# Comprehensive Tests
test-all-happy:
	@echo "$(YELLOW)Running all happy path tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/test-suites/all-happy-paths.yaml \
		$$ENV_VARS \
		--format junit \
		--output reports/all-happy-$(ENV)

test-all:
	@echo "$(YELLOW)Running all tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/ flows/features/auth/negative/ flows/features/auth/edge-cases/ \
		$$ENV_VARS \
		--format junit \
		--output reports/all-tests-$(ENV)

# Custom tag testing
test-by-tag:
	@if [ -z "$(INCLUDE_TAGS)" ] && [ -z "$(EXCLUDE_TAGS)" ]; then \
		echo "$(RED)Error: INCLUDE_TAGS or EXCLUDE_TAGS parameter required.$(NC)"; \
		echo "$(YELLOW)Usage examples:$(NC)"; \
		echo "  make test-by-tag INCLUDE_TAGS=\"feature:auth\""; \
		echo "  make test-by-tag INCLUDE_TAGS=\"priority:p0,platform:ios\""; \
		echo "  make test-by-tag EXCLUDE_TAGS=\"priority:p3\""; \
		echo "  make test-by-tag INCLUDE_TAGS=\"feature:auth\" EXCLUDE_TAGS=\"negative\""; \
		exit 1; \
	fi
	@TAG_ARGS=""; \
	if [ -n "$(INCLUDE_TAGS)" ]; then \
		TAG_ARGS="$$TAG_ARGS --include-tags=$(INCLUDE_TAGS)"; \
		echo "$(YELLOW)Including tags: $(INCLUDE_TAGS)$(NC)"; \
	fi; \
	if [ -n "$(EXCLUDE_TAGS)" ]; then \
		TAG_ARGS="$$TAG_ARGS --exclude-tags=$(EXCLUDE_TAGS)"; \
		echo "$(YELLOW)Excluding tags: $(EXCLUDE_TAGS)$(NC)"; \
	fi; \
	echo "$(YELLOW)Running tests with tag filters on $(ENV)...$(NC)"; \
	ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/ flows/features/auth/negative/ flows/features/auth/edge-cases/ \
		$$TAG_ARGS \
		$$ENV_VARS \
		--format junit \
		--output reports/tag-$(ENV)

# Priority testing
test-p0:
	@echo "$(YELLOW)Running P0 priority tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/ flows/features/auth/negative/ flows/features/auth/edge-cases/ \
		--include-tags="priority:p0" \
		$$ENV_VARS \
		--format junit \
		--output reports/p0-$(ENV)

test-p1:
	@echo "$(YELLOW)Running P1 priority tests on $(ENV)...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/ flows/features/auth/negative/ flows/features/auth/edge-cases/ \
		--include-tags="priority:p1" \
		$$ENV_VARS \
		--format junit \
		--output reports/p1-$(ENV)

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
	@make test-smoke ENV=dev

staging-smoke:
	@echo "$(YELLOW)Running smoke tests in staging mode...$(NC)"
	@make test-smoke ENV=staging

prod-smoke:
	@echo "$(YELLOW)Running smoke tests in production mode...$(NC)"
	@make test-smoke ENV=prod

# Quick test commands
quick-auth:
	@echo "$(YELLOW)Running quick auth validation...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
	maestro test flows/features/auth/happy-path/sign-up-flow.yaml \
		$$ENV_VARS

quick-ios: check-ios-simulator install-app
	@echo "$(YELLOW)Running quick iOS validation...$(NC)"
	@ENV_VARS=$$($(MAKE) -s extract-env-vars ENV=$(ENV)); \
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
	@if [ ! -f "configs/env-$(ENV).yaml" ]; then \
		echo "$(RED)Config file not found: configs/env-$(ENV).yaml$(NC)"; \
		exit 1; \
	fi; \
	grep -A 20 "^env:" configs/env-$(ENV).yaml | grep "^  [A-Z_]" | sed 's/^  /-e /;s/: */=/;s/"//g' | tr '\n' ' '