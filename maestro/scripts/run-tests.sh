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
SUITE=${2:-"smoke"}
OUTPUT_DIR="reports"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

echo -e "${YELLOW}Maestro Test Runner${NC}"
echo -e "${YELLOW}Environment: ${ENV}${NC}"
echo -e "${YELLOW}Suite: ${SUITE}${NC}"
echo ""

case "$SUITE" in
  "smoke")
    echo -e "${GREEN}Running smoke test suite...${NC}"
    maestro test flows/quality-gates/smoke-suite.yaml \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/smoke-$ENV
    ;;
  "smoke-ios")
    echo -e "${GREEN}Running iOS smoke test suite...${NC}"
    maestro test flows/quality-gates/smoke-suite-ios.yaml \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/smoke-ios-$ENV
    ;;
  "regression")
    echo -e "${GREEN}Running daily regression suite...${NC}"
    maestro test flows/quality-gates/daily-regression.yaml \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/regression-$ENV
    ;;
  "auth-all")
    echo -e "${GREEN}Running all authentication tests...${NC}"
    maestro test flows/test-suites/auth-all.yaml \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/auth-all-$ENV
    ;;
  "auth-happy")
    echo -e "${GREEN}Running authentication happy path tests...${NC}"
    maestro test flows/features/auth/happy-path/ \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/auth-happy-$ENV
    ;;
  "auth-ios")
    echo -e "${GREEN}Running iOS authentication tests...${NC}"
    maestro test flows/test-suites/auth-ios.yaml \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/auth-ios-$ENV
    ;;
  "all-happy")
    echo -e "${GREEN}Running all happy path tests...${NC}"
    maestro test flows/test-suites/all-happy-paths.yaml \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/all-happy-$ENV
    ;;
  "ios")
    echo -e "${GREEN}Running all iOS tests...${NC}"
    maestro test flows/features/ \
      --tags "platform:ios" \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/ios-all-$ENV
    ;;
  "android")
    echo -e "${GREEN}Running all Android tests...${NC}"
    maestro test flows/features/ \
      --tags "platform:android" \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/android-all-$ENV
    ;;
  "cross-platform")
    echo -e "${GREEN}Running cross-platform tests...${NC}"
    maestro test flows/features/ \
      --tags "platform:ios and platform:android" \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/cross-platform-$ENV
    ;;
  "p0")
    echo -e "${GREEN}Running P0 priority tests...${NC}"
    maestro test flows/features/ \
      --tags "priority:p0" \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/p0-$ENV
    ;;
  "p1")
    echo -e "${GREEN}Running P1 priority tests...${NC}"
    maestro test flows/features/ \
      --tags "priority:p1" \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/p1-$ENV
    ;;
  "by-tag")
    if [ -z "$3" ]; then
      echo -e "${RED}Error: Tag parameter required for by-tag suite${NC}"
      echo -e "${YELLOW}Usage: ./run-tests.sh staging by-tag \"feature:auth\"${NC}"
      exit 1
    fi
    echo -e "${GREEN}Running tests with tag: $3...${NC}"
    maestro test flows/features/ \
      --tags "$3" \
      --env-file configs/env-$ENV.yaml \
      --format junit \
      --output $OUTPUT_DIR/tag-$ENV
    ;;
  *)
    echo -e "${RED}Unknown suite: $SUITE${NC}"
    echo ""
    echo -e "${YELLOW}Available suites:${NC}"
    echo "  smoke           - Critical path smoke tests"
    echo "  smoke-ios       - iOS-specific smoke tests"
    echo "  regression      - Daily regression suite"
    echo "  auth-all        - All authentication tests"
    echo "  auth-happy      - Authentication happy paths"
    echo "  auth-ios        - iOS authentication tests"
    echo "  all-happy       - All happy path tests"
    echo "  ios             - All iOS tests"
    echo "  android         - All Android tests"
    echo "  cross-platform  - Cross-platform tests"
    echo "  p0              - Priority P0 tests"
    echo "  p1              - Priority P1 tests"
    echo "  by-tag          - Tests by custom tag"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./run-tests.sh [environment] [suite] [tag]"
    echo "  Examples:"
    echo "    ./run-tests.sh staging smoke"
    echo "    ./run-tests.sh dev auth-all"
    echo "    ./run-tests.sh staging by-tag \"feature:auth and priority:p1\""
    exit 1
    ;;
esac

echo -e "${GREEN}Test execution completed!${NC}"
echo -e "${YELLOW}Reports saved to: $OUTPUT_DIR/${NC}"