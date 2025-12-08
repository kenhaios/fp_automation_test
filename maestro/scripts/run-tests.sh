#!/bin/bash
# Maestro Test Runner Script
# Provides flexible test execution with environment and suite selection

set -e

# Colors for output
YELLOW='\033[1;33m'
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m' # No Color

# Default values
ENV=${1:-"staging"}
SUITE=${2:-"smoke-ios"}
OUTPUT_DIR="reports"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

echo -e "${YELLOW}Maestro Test Runner${NC}"
echo -e "${YELLOW}Environment: ${ENV}${NC}"
echo -e "${YELLOW}Suite: ${SUITE}${NC}"
echo ""

# Function to get appropriate environment file
get_env_file() {
    local suite=$1
    local env=$2
    
    case "$suite" in
        *-ios|smoke-ios|auth-ios)
            echo "configs/env-${env}-ios.yaml"
            ;;
        *-android|smoke-android|auth-android)
            echo "configs/env-${env}-android.yaml"
            ;;
        *)
            echo "configs/env-${env}-ios.yaml"  # Default to iOS for legacy compatibility
            ;;
    esac
}

# Function to extract environment variables for maestro
extract_env_vars() {
    local config_file=$1
    
    if [ ! -f "$config_file" ]; then
        echo -e "${RED}Config file not found: $config_file${NC}"
        echo -e "${YELLOW}Available config files:${NC}"
        ls configs/env-*.yaml 2>/dev/null || echo "  No config files found"
        exit 1
    fi
    
    grep -A 20 "^env:" "$config_file" | grep "^  [A-Z_]" | sed 's/^  /-e /;s/: */=/;s/"//g' | tr '\n' ' '
}

case "$SUITE" in
  "smoke-ios")
    echo -e "${GREEN}Running iOS smoke test suite...${NC}"
    ENV_FILE=$(get_env_file $SUITE $ENV)
    ENV_VARS=$(extract_env_vars $ENV_FILE)
    echo -e "${YELLOW}Using environment file: $ENV_FILE${NC}"
    maestro test flows/quality-gates/smoke-suite-ios.yaml \
      $ENV_VARS \
      --format junit \
      --output $OUTPUT_DIR/smoke-ios-$ENV
    ;;
  "smoke-android")
    echo -e "${GREEN}Running Android smoke test suite...${NC}"
    ENV_FILE=$(get_env_file $SUITE $ENV)
    ENV_VARS=$(extract_env_vars $ENV_FILE)
    echo -e "${YELLOW}Using environment file: $ENV_FILE${NC}"
    maestro test flows/quality-gates/smoke-suite-android.yaml \
      $ENV_VARS \
      --format junit \
      --output $OUTPUT_DIR/smoke-android-$ENV
    ;;
  "regression-mobile")
    echo -e "${GREEN}Running mobile regression test suite (iOS & Android)...${NC}"
    
    # Run iOS regression
    ENV_FILE_IOS=$(get_env_file "smoke-ios" $ENV)
    ENV_VARS_IOS=$(extract_env_vars $ENV_FILE_IOS)
    echo -e "${YELLOW}Running iOS regression tests...${NC}"
    maestro test flows/quality-gates/daily-regression.yaml \
      $ENV_VARS_IOS \
      --include-tags="platform:ios" \
      --format junit \
      --output $OUTPUT_DIR/regression-ios-$ENV
    
    # Run Android regression
    ENV_FILE_ANDROID=$(get_env_file "smoke-android" $ENV)
    ENV_VARS_ANDROID=$(extract_env_vars $ENV_FILE_ANDROID)
    echo -e "${YELLOW}Running Android regression tests...${NC}"
    maestro test flows/quality-gates/daily-regression.yaml \
      $ENV_VARS_ANDROID \
      --include-tags="platform:android" \
      --format junit \
      --output $OUTPUT_DIR/regression-android-$ENV
    ;;
  "auth-ios")
    echo -e "${GREEN}Running iOS authentication test suite...${NC}"
    ENV_FILE=$(get_env_file $SUITE $ENV)
    ENV_VARS=$(extract_env_vars $ENV_FILE)
    echo -e "${YELLOW}Using environment file: $ENV_FILE${NC}"
    maestro test flows/test-suites/auth-ios.yaml \
      $ENV_VARS \
      --format junit \
      --output $OUTPUT_DIR/auth-ios-$ENV
    ;;
  "auth-android")
    echo -e "${GREEN}Running Android authentication test suite...${NC}"
    ENV_FILE=$(get_env_file $SUITE $ENV)
    ENV_VARS=$(extract_env_vars $ENV_FILE)
    echo -e "${YELLOW}Using environment file: $ENV_FILE${NC}"
    maestro test flows/test-suites/auth-android.yaml \
      $ENV_VARS \
      --format junit \
      --output $OUTPUT_DIR/auth-android-$ENV
    ;;
  *)
    echo -e "${RED}Unknown suite: $SUITE${NC}"
    echo ""
    echo -e "${YELLOW}Available suites:${NC}"
    echo ""
    echo -e "${GREEN}Quality Gates:${NC}"
    echo "  smoke-ios        - iOS critical path smoke tests"
    echo "  smoke-android    - Android critical path smoke tests" 
    echo "  regression-mobile - Daily regression suite for both platforms"
    echo ""
    echo -e "${GREEN}Platform-Specific Test Suites:${NC}"
    echo "  auth-ios         - iOS authentication test suite"
    echo "  auth-android     - Android authentication test suite"
    echo ""
    echo -e "${GREEN}Available Test Suites:${NC}"
    echo -e "${YELLOW}iOS Suites:${NC}"
    ls flows/test-suites/*ios*.yaml 2>/dev/null | sed 's/flows\/test-suites\///g; s/\.yaml//g' | sed 's/^/  /' || echo "  No iOS test suites found"
    echo -e "${YELLOW}Android Suites:${NC}"
    ls flows/test-suites/*android*.yaml 2>/dev/null | sed 's/flows\/test-suites\///g; s/\.yaml//g' | sed 's/^/  /' || echo "  No Android test suites found"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./run-tests.sh [environment] [suite]"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./run-tests.sh staging smoke-ios"
    echo "  ./run-tests.sh dev smoke-android" 
    echo "  ./run-tests.sh staging auth-ios"
    echo "  ./run-tests.sh dev auth-android"
    echo "  ./run-tests.sh staging regression-mobile"
    echo ""
    echo -e "${YELLOW}Environment options:${NC}"
    echo "  dev      - Development environment"
    echo "  staging  - Staging environment (default)"
    echo "  prod     - Production environment"
    exit 1
    ;;
esac

echo -e "${GREEN}Test execution completed!${NC}"
echo -e "${YELLOW}Reports saved to: $OUTPUT_DIR/${NC}"