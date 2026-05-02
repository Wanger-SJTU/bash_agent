.PHONY: help install test test-unit test-system run clean lint format install-hooks check-secrets

help:
	@echo "Bashagnet Development Commands:"
	@echo "  make install       - Install dependencies with uv"
	@echo "  make test          - Run all tests"
	@echo "  make test-unit     - Run unit tests only"
	@echo "  make test-system   - Run system tests only"
	@echo "  make install-hooks - Install git pre-commit hooks"
	@echo "  make check-secrets - Manually check for secrets"
	@echo "  make run           - Run bashagnet (example)"
	@echo "  make lint          - Run linter"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean up cache files"

install:
	uv sync

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit -v

test-system:
	uv run pytest tests/system -v

test-coverage:
	uv run pytest --cov=bashagnet --cov-report=html

install-hooks:
	@echo "Installing git hooks..."
	./scripts/install-hooks.sh

check-secrets:
	@echo "Checking for secrets in tracked files..."
	@./scripts/check-secrets.sh || exit 1

run:
	uv run bashagnet --help

run-interactive:
	uv run bashagnet --interactive

lint:
	uv run ruff check bashagnet/

format:
	uv run black bashagnet/
	uv run ruff check --fix bashagnet/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov
