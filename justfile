# List available commands
default:
    @just --list

# Run all tests
test:
    uv run pytest

# Run unit tests only
test-unit:
    uv run pytest tests/unit

# Run integration tests only
test-integration:
    uv run pytest tests/integration

# Run tests with coverage
test-coverage:
    uv run pytest --cov=project --cov-report=html --cov-report=term

# Run all code quality checks (lint, type-check, test)
check: lint type-check test

# Lint code
lint:
    uv run ruff check .

# Fix linting issues
lint-fix:
    uv run ruff check . --fix

# Format code
format:
    uv run ruff format .

# Type check
type-check:
    uv run ty check

# Run pre-commit hooks
pre-commit:
    pre-commit run --all-files

# Install pre-commit hooks
pre-commit-install:
    pre-commit install

# Install dependencies
install:
    uv sync --dev

# Install dependencies without dev group
install-prod:
    uv sync

# Clean build artifacts and caches
clean:
    rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build
    find . -type d -name __pycache__ -exec rm -rf {} +

# Check licenses
license-check:
    uv run licensecheck

# Run the project
run:
    uv run project

# Build Docker image
docker-build:
    docker build -t project .

# Run Docker container
docker-run:
    docker run project

# Build and run Docker
docker: docker-build docker-run
