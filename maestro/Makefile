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
	@echo "$(GREEN)Utility:$(NC)"
	@echo "  make clean              - Clean reports and screenshots"
	@echo "  make validate-tags      - Validate test tags"
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
	maestro test flows/quality-gates/smoke-suite.yaml \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/smoke-$(ENV)

test-smoke-ios:
	@echo "$(YELLOW)Running iOS smoke tests on $(ENV)...$(NC)"
	maestro test flows/quality-gates/smoke-suite-ios.yaml \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/smoke-ios-$(ENV)

test-regression:
	@echo "$(YELLOW)Running daily regression suite on $(ENV)...$(NC)"
	maestro test flows/quality-gates/daily-regression.yaml \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/regression-$(ENV)

# Feature Tests
test-auth:
	@echo "$(YELLOW)Running all authentication tests on $(ENV)...$(NC)"
	maestro test flows/test-suites/auth-all.yaml \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/auth-all-$(ENV)

test-auth-happy:
	@echo "$(YELLOW)Running authentication happy path tests on $(ENV)...$(NC)"
	maestro test flows/features/auth/happy-path/ \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/auth-happy-$(ENV)

# Platform-Specific Tests
test-ios:
	@echo "$(YELLOW)Running all iOS tests on $(ENV)...$(NC)"
	maestro test flows/features/ \
		--tags "platform:ios" \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/ios-all-$(ENV)

test-android:
	@echo "$(YELLOW)Running all Android tests on $(ENV)...$(NC)"
	maestro test flows/features/ \
		--tags "platform:android" \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/android-all-$(ENV)

test-cross:
	@echo "$(YELLOW)Running cross-platform tests on $(ENV)...$(NC)"
	maestro test flows/features/ \
		--tags "platform:ios and platform:android" \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/cross-platform-$(ENV)

# Comprehensive Tests
test-all-happy:
	@echo "$(YELLOW)Running all happy path tests on $(ENV)...$(NC)"
	maestro test flows/test-suites/all-happy-paths.yaml \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/all-happy-$(ENV)

test-all:
	@echo "$(YELLOW)Running all tests on $(ENV)...$(NC)"
	maestro test flows/features/ \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/all-tests-$(ENV)

# Custom tag testing
test-by-tag:
	@if [ -z "$(TAG)" ]; then \
		echo "$(RED)Error: TAG parameter required. Usage: make test-by-tag TAG=\"feature:auth\"$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Running tests with tag: $(TAG) on $(ENV)...$(NC)"
	maestro test flows/features/ \
		--tags "$(TAG)" \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/tag-$(ENV)

# Priority testing
test-p0:
	@echo "$(YELLOW)Running P0 priority tests on $(ENV)...$(NC)"
	maestro test flows/features/ \
		--tags "priority:p0" \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/p0-$(ENV)

test-p1:
	@echo "$(YELLOW)Running P1 priority tests on $(ENV)...$(NC)"
	maestro test flows/features/ \
		--tags "priority:p1" \
		--env-file configs/env-$(ENV).yaml \
		--format junit \
		--output reports/p1-$(ENV)

# Utility commands
clean:
	@echo "$(YELLOW)Cleaning reports and screenshots...$(NC)"
	@rm -rf reports/* screenshots/*
	@echo "$(GREEN)Clean complete!$(NC)"

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
	maestro test flows/features/auth/happy-path/sign-up-flow.yaml \
		--env-file configs/env-$(ENV).yaml

quick-ios:
	@echo "$(YELLOW)Running quick iOS validation...$(NC)"
	maestro test flows/features/auth/happy-path/sign-in-ios.yaml \
		--env-file configs/env-$(ENV).yaml