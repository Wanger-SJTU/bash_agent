#!/bin/bash
# Development helper script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

case "${1:-help}" in
    install)
        echo -e "${BLUE}Installing dependencies...${NC}"
        uv sync
        ;;
    test)
        echo -e "${BLUE}Running all tests...${NC}"
        uv run pytest
        ;;
    test-unit)
        echo -e "${BLUE}Running unit tests...${NC}"
        uv run pytest tests/unit -v
        ;;
    test-system)
        echo -e "${BLUE}Running system tests...${NC}"
        uv run pytest tests/system -v
        ;;
    run)
        shift
        echo -e "${BLUE}Running bashagnet...${NC}"
        uv run bashagnet "$@"
        ;;
    interactive)
        echo -e "${GREEN}Starting interactive mode...${NC}"
        uv run bashagnet --interactive
        ;;
    lint)
        echo -e "${BLUE}Linting...${NC}"
        uv run ruff check bashagnet/
        ;;
    format)
        echo -e "${BLUE}Formatting...${NC}"
        uv run black bashagnet/
        uv run ruff check --fix bashagnet/
        ;;
    help|*)
        echo "Bashagnet Development Script"
        echo ""
        echo "Usage: ./scripts/dev.sh [command]"
        echo ""
        echo "Commands:"
        echo "  install       Install dependencies"
        echo "  test          Run all tests"
        echo "  test-unit     Run unit tests only"
        echo "  test-system   Run system tests only"
        echo "  run [args]    Run bashagnet with arguments"
        echo "  interactive   Start interactive mode"
        echo "  lint          Run linter"
        echo "  format        Format code"
        echo "  help          Show this help"
        ;;
esac
