# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project using UV for dependency management. The project requires Python 3.13+ and uses a modern tooling setup with pre-commit hooks for code quality.

## Essential Commands

### Task Runner (Just)

The project uses [Just](https://github.com/casey/just) as a command runner for common tasks. Just provides a convenient way to run project commands and is especially useful in CI/CD pipelines.

**Installation:**

Just is included as a dev dependency (`rust-just` package) and will be automatically installed when you run `uv sync --dev`. No separate installation needed!

**Usage:**
- **List all commands**: `just` or `just --list`
- **Run tests**: `just test` (all), `just test-unit` (unit only), `just test-integration` (integration only)
- **Run quality checks**: `just check` (runs lint, type-check, and test)
- **Format and lint**: `just format`, `just lint`, `just lint-fix`
- **Type check**: `just type-check`
- **Install dependencies**: `just install`
- **Clean artifacts**: `just clean`
- **Run project**: `just run`
- **Docker**: `just docker-build`, `just docker-run`, `just docker` (build + run)

All Just commands are defined in the `justfile` at the project root. You can also use the UV commands directly (see below) if you prefer.

### Dependency Management
- **Install dependencies**: `uv sync`
- **Install with dev dependencies**: `uv sync --dev` (dev dependencies are in the `dev` dependency group)
- **Add a new dependency**: `uv add <package-name>`
- **Add a dev dependency**: `uv add --dev <package-name>`

### Running the Project
- **Run the project**: `uv run project` (uses console script entry point)
- **Run as a module**: `uv run python -m project` (alternative method)
- **Run with Docker**: `docker build -t project . && docker run project`

### Testing
- **Run all tests**: `uv run pytest`
- **Run specific test file**: `uv run pytest tests/unit/test_example.py`

#### Testing Guidelines

**Framework and Structure**
- Use pytest exclusively - do NOT use the unittest module
- Do NOT group tests in classes - write standalone test functions
- Place unit tests in `tests/unit/` and integration tests in `tests/integration/`

**Type Annotations**
- All test functions must include type annotations for parameters and return values
- When using mocks, annotate them with the expected type they're mocking, NOT as `Mock`
  ```python
  def test_example(mock_service: ServiceClass) -> None:
      # mock_service is typed as ServiceClass, not Mock
  ```

**Mocking**
- Mock external resources and services that may not be available during CI runs (databases, APIs, file systems, network calls)
- Use `pytest-mock` for mocking
- Type mocks as the interface they're replacing, not as Mock objects

**Fixtures**
- Use pytest fixtures for test setup and reusable test data
- Define shared fixtures in `conftest.py` files for reuse across multiple test files
- Prefer fixtures over setup/teardown methods

**Test Style**
- Keep tests concise - focus on the most important cases, not exhaustive coverage
- Skip redundant tests (e.g., don't test class initialization if it's tested elsewhere)
- Do NOT add docstrings or comments to test functions - test names should be self-explanatory
- Use descriptive test function names that explain what is being tested

**Best Practices**
- Each test should verify one specific behavior or scenario
- Use `assert` statements directly - pytest provides helpful assertion introspection
- Prefer parametrized tests (`@pytest.mark.parametrize`) for testing multiple similar cases
- Keep test data close to the test - use fixtures or inline data
- Tests should be independent and able to run in any order

**Verification**
- ALWAYS run `uv run pytest` after making any changes to verify tests pass
- Ensure tests work in isolation and don't depend on execution order
- Check that mocked resources don't cause tests to fail in CI environments

### Code Quality
- **Run pre-commit hooks**: `pre-commit run --all-files`
- **Install pre-commit hooks**: `pre-commit install`
- **Type checking**: `uv run ty check`
- **Format code**: `uv run ruff format .`
- **Lint code**: `uv run ruff check . --fix`
- **Check licenses**: `uv run licensecheck`

## Architecture

### Project Structure
- `src/project/`: Main application code
  - `__main__.py`: Entry point containing the `main()` function (works with both run methods)
  - `__init__.py`: Package initialization (version info, etc.)
  - `config.py`: Configuration management (nearly empty placeholder)
- `tests/`: Test suite
  - `unit/`: Unit tests
  - `integration/`: Integration tests
  - `conftest.py`: Pytest configuration and fixtures

### Configuration Management
The project uses TOML files in the `configs/` directory for configuration. Environment variables can be set via `.env` files (use `.env.example` as a template).

### Logging
The project uses `loguru` for logging. The Docker environment sets `LOGURU_LEVEL="INFO"` by default.

### Pre-commit Hooks
The project enforces code quality through several pre-commit hooks:
- **pre-commit-hooks**: Standard checks including case conflicts, merge conflicts, trailing whitespace, AST validation, large files, end-of-file fixer, and TOML/JSON/YAML validation
- **ruff**: Multi-stage linting and formatting
  - `ruff-check` with `--fix` for general linting (excludes tests)
  - `ruff-check` with `--select I --fix` for import sorting (excludes test data)
  - `ruff-format` for code formatting (excludes test data)
- **bandit**: Security vulnerability scanning with recursive scanning (excludes tests)
- **pyupgrade**: Automatically upgrades Python syntax to 3.13+ standards
- **ty**: Type checking using the ty type checker (runs on all Python files)
- **licensecheck**: Verifies dependency licenses and generates `DEPS_LICENSES.md` (runs when pyproject.toml changes)

### Ruff Configuration
The project uses Ruff for linting and formatting with the following configuration:
- **Line length**: 120 characters
- **Docstring formatting**: Enabled with Google convention (code blocks in docstrings are formatted)
- **Preview mode**: Enabled for access to latest rules
- **Selected rule sets**: pycodestyle (E/W), Pyflakes (F), flake8-comprehensions (C4), mccabe (C90), pydocstyle (D), isort (I), flake8-pytest-style (PT), Pylint (PL), flake8-simplify (SIM), pyupgrade (UP), flake8-bandit (S), flake8-annotations (ANN), flake8-bugbear (B), NumPy-specific rules (NPY), and selected preview rules
- **Ignored rules**: Some docstring requirements (D100, D104, D105, D107) and annotation requirements for *args/**kwargs
- **Per-file ignores**: Tests ignore security assertions (S101), missing docstrings (D103), and some complexity rules

### Type Checking Configuration
The project uses **ty** (not mypy) for type checking with the following configuration:
- **Python version**: 3.13
- **Source files**: `src/**/*.py`
- **Type ignore comments**: Respected (allows `# type: ignore`)
- **Error handling**: Does not fail on warnings, only on errors
- **Output format**: Full
- **Rules**:
  - `possibly-unresolved-reference`: error
  - `index-out-of-bounds`: error

Run type checking with `uv run ty check` or let pre-commit handle it automatically.

### License
The project uses a PROPRIETARY license. Dependencies are tracked in `DEPS_LICENSES.md` via licensecheck.
