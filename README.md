# Python Project Template

A modern, production-ready Python project template with comprehensive tooling for code quality, testing, and deployment.

## Table of Contents

- [Python Project Template](#python-project-template)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Technology Stack](#technology-stack)
    - [Core Dependencies](#core-dependencies)
    - [Development Tools](#development-tools)
    - [Container \& Deployment](#container--deployment)
  - [Prerequisites](#prerequisites)
  - [Quick Start](#quick-start)
    - [1. Clone and Setup](#1-clone-and-setup)
    - [2. Configure Environment](#2-configure-environment)
    - [3. Run the Project](#3-run-the-project)
  - [Project Structure](#project-structure)
  - [Configuration](#configuration)
    - [Example Configuration](#example-configuration)
    - [Environment Variables](#environment-variables)
  - [Development Workflow](#development-workflow)
    - [Running the Project](#running-the-project)
    - [Testing](#testing)
    - [Code Quality](#code-quality)
      - [Run All Checks](#run-all-checks)
      - [Individual Tools](#individual-tools)
    - [Dependency Management](#dependency-management)
  - [Docker](#docker)
    - [Build and Run](#build-and-run)
    - [Docker Configuration](#docker-configuration)
  - [Pre-commit Hooks](#pre-commit-hooks)
    - [Hook Pipeline](#hook-pipeline)
    - [Configuration](#configuration-1)
  - [License](#license)

## Overview

This is a template Python project built with modern best practices and tooling. It provides a solid foundation for building Python applications with:

- Fast dependency management with **UV**
- Comprehensive code quality checks with **Ruff**, **Bandit**, and **ty**
- Automated testing with **pytest**
- Docker containerization
- Pre-commit hooks for consistent code quality
- Type checking and security scanning

## Technology Stack

### Core Dependencies
- **Python 3.13+** - Latest Python version with modern language features
- **UV** - Fast Python package installer and resolver
- **Loguru** - Advanced logging with structured output
- **Pydantic** - Data validation using Python type annotations
- **Pydantic Settings** - Settings management with environment variable support

### Development Tools
- **Ruff** - Extremely fast Python linter and formatter (replaces Black, isort, flake8, and more)
- **Pytest** - Testing framework with pytest-mock for mocking
- **ty** - Modern type checker for Python
- **Bandit** - Security vulnerability scanner
- **Pre-commit** - Git hook framework for automated checks
- **pyupgrade** - Automatic Python syntax upgrading to 3.13+
- **licensecheck** - Dependency license verification

### Container & Deployment
- **Docker** - Containerization with multi-stage builds
- **GitHub Actions** - CI/CD ready (hooks in place)

## Prerequisites

- **Python 3.13 or higher**
- **UV** - Install from [astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/)
- **Docker** (optional) - For containerized deployment
- **Git** - For version control and pre-commit hooks

**Note:** Just (command runner) is included as a dev dependency and will be automatically installed with `uv sync --dev`.

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd python-template

# Install dependencies
uv sync

# Install pre-commit hooks
pre-commit install
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# EXAMPLE_ENVVAR=your-value
# NESTED__SOME_NESTED_ENVVAR=nested-value
```

### 3. Run the Project

```bash
# Run using the console script entry point
uv run project

# Or run as a module
uv run python -m project
```

## Project Structure

```
python-template/
├── src/
│   └── project/              # Main application package
│       ├── __init__.py       # Package initialization
│       ├── __main__.py       # Entry point with main() function
│       └── config.py         # Configuration management with Pydantic
├── tests/
│   ├── unit/                 # Unit tests
│   │   ├── __init__.py
│   │   └── test_config.py
│   ├── integration/          # Integration tests
│   │   ├── __init__.py
│   │   └── test_dockerfile.py
│   └── conftest.py           # Pytest configuration and shared fixtures
├── scripts/                  # Utility scripts
│   └── example.sh
├── docs/                     # Documentation
├── .env.example              # Example environment variables
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── Dockerfile                # Docker container definition
├── pyproject.toml            # Project metadata and tool configuration
├── uv.lock                   # Locked dependency versions
├── CLAUDE.md                 # AI assistant instructions
├── DEPS_LICENSES.md          # Auto-generated dependency licenses
├── LICENSE                   # Project license
└── README.md                 # This file
```

## Configuration

The project uses **Pydantic Settings** for configuration management, supporting:

- Environment variables from `.env` files
- Nested configuration with double underscore delimiter (`NESTED__VAR`)
- Type validation and secret handling
- Default values with field descriptions

### Example Configuration

```python
# config.py
class Settings(BaseSettings):
    some_example_var: int = Field(5, description="Some value")
    example_envvar: SecretStr = Field(..., description="Example of secret envvar")
    nested: NestedSettings = Field(default_factory=NestedSettings)
```

### Environment Variables

```bash
# .env
SOME_EXAMPLE_VAR=10
EXAMPLE_ENVVAR=secret-value
NESTED__SOME_NESTED_ENVVAR=nested-value
```

## Task Runner (Just)

The project includes a [`justfile`](https://github.com/casey/just) with convenient commands for common tasks. Just is a modern command runner that makes it easy to run project tasks consistently across development and CI/CD.

Just is installed automatically as a dev dependency (`rust-just` package) when you run `uv sync --dev`.

**Quick Reference:**

```bash
# List all available commands
just

# Testing
just test                # Run all tests
just test-unit           # Run unit tests only
just test-integration    # Run integration tests only
just test-coverage       # Run tests with coverage report

# Code Quality
just check               # Run all checks (lint, type-check, test)
just lint                # Lint code
just lint-fix            # Fix linting issues
just format              # Format code
just type-check          # Run type checking
just pre-commit          # Run pre-commit hooks

# Development
just install             # Install dependencies with dev group
just install-prod        # Install production dependencies only
just run                 # Run the project
just clean               # Clean build artifacts and caches

# Docker
just docker-build        # Build Docker image
just docker-run          # Run Docker container
just docker              # Build and run (combined)
```

All commands use UV under the hood, so you can also run UV commands directly if you prefer (see sections below).

## Development Workflow

### Running the Project

```bash
# Using console script (recommended)
uv run project

# As a Python module
uv run python -m project

# With Docker
docker build -t project . && docker run project
```

### Testing

The project uses **pytest** for testing with the following guidelines:

- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- All test functions must have type annotations
- Mock external resources using `pytest-mock`
- No test classes - use standalone functions
- Fixtures in `conftest.py` for shared setup

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_config.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=project
```

### Code Quality

#### Run All Checks

```bash
# Run all pre-commit hooks
pre-commit run --all-files
```

#### Individual Tools

```bash
# Type checking with ty
uv run ty check

# Format code with Ruff
uv run ruff format .

# Lint code with Ruff
uv run ruff check . --fix

# Security scanning with Bandit
bandit -r src/

# Check dependency licenses
uv run licensecheck
```

### Dependency Management

```bash
# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Update dependencies
uv sync

# Update with dev dependencies
uv sync --dev
```

## Docker

The project includes a multi-stage Dockerfile optimized for production:

### Build and Run

```bash
# Build the Docker image
docker build -t project .

# Run the container
docker run project

# Run with environment variables
docker run -e EXAMPLE_ENVVAR=value project

# Run interactively
docker run -it project /bin/bash
```

### Docker Configuration

- Base image: `python:3.13-slim-bullseye`
- UV package manager included
- Frozen dependency installation for reproducibility
- Default log level: `INFO` (via `LOGURU_LEVEL`)

## Pre-commit Hooks

The project enforces code quality through automated pre-commit hooks:

### Hook Pipeline

1. **Standard Checks** (pre-commit-hooks)
   - Case conflict detection
   - Merge conflict detection
   - Trailing whitespace removal
   - AST validation
   - Large file detection
   - TOML/JSON/YAML validation
   - End-of-file fixer

2. **Ruff Multi-stage**
   - General linting with auto-fix (excludes tests)
   - Import sorting (excludes test data)
   - Code formatting (excludes test data)

3. **Security Scanning** (Bandit)
   - Recursive security vulnerability scanning
   - Excludes tests directory

4. **Python Upgrade** (pyupgrade)
   - Automatic syntax upgrade to Python 3.13+

5. **Type Checking** (ty)
   - Static type analysis on all Python files

6. **License Checking** (licensecheck)
   - Dependency license verification
   - Generates `DEPS_LICENSES.md`

### Configuration

Hooks are configured in `.pre-commit-config.yaml`. To modify behavior, edit this file and run:

```bash
pre-commit install
```

## License

This project uses a **PROPRIETARY** license. See [LICENSE](LICENSE) for details.

Dependency licenses are tracked in [DEPS_LICENSES.md](DEPS_LICENSES.md).

---

**Note**: This is a template project. Update this README with your specific project details, including:
- Actual project name and description
- Repository URL
- Specific configuration requirements
- Deployment instructions
- Contributing guidelines
- Contact information
