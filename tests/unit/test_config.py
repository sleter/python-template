import pytest
from pydantic import ValidationError
from pytest_mock import MockerFixture

from project.config import NestedSettings, Settings


@pytest.fixture
def valid_env_vars() -> dict[str, str]:
    return {
        "EXAMPLE_ENVVAR": "secret-value-123",
        "NESTED__SOME_NESTED_ENVVAR": "nested-value-456",
    }


@pytest.fixture
def valid_env_vars_with_override() -> dict[str, str]:
    return {
        "EXAMPLE_ENVVAR": "secret-value-123",
        "NESTED__SOME_NESTED_ENVVAR": "nested-value-456",
        "SOME_EXAMPLE_VAR": "42",
    }


def test_settings_initialization_with_required_env_vars(mocker: MockerFixture, valid_env_vars: dict[str, str]) -> None:
    mocker.patch.dict("os.environ", valid_env_vars)

    settings = Settings()

    assert settings.some_example_var == 5
    assert settings.example_envvar.get_secret_value() == "secret-value-123"
    assert settings.nested.some_nested_envvar == "nested-value-456"


def test_settings_with_overridden_default_value(
    mocker: MockerFixture,
    valid_env_vars_with_override: dict[str, str],
) -> None:
    mocker.patch.dict("os.environ", valid_env_vars_with_override)

    settings = Settings()

    assert settings.some_example_var == 42
    assert settings.example_envvar.get_secret_value() == "secret-value-123"


def test_settings_missing_required_example_envvar(
    mocker: MockerFixture,
) -> None:
    mocker.patch.dict("os.environ", {"NESTED__SOME_NESTED_ENVVAR": "nested-value"})

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("example_envvar",) for error in errors)


def test_settings_missing_required_nested_envvar(
    mocker: MockerFixture,
) -> None:
    mocker.patch.dict("os.environ", {"EXAMPLE_ENVVAR": "secret-value"})

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("some_nested_envvar",) for error in errors)


def test_settings_missing_all_required_env_vars(mocker: MockerFixture) -> None:
    mocker.patch.dict("os.environ", {}, clear=True)

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    errors = exc_info.value.errors()
    assert len(errors) >= 1
    error_locs = [tuple(error["loc"]) for error in errors]
    assert ("some_nested_envvar",) in error_locs


def test_settings_default_value_for_some_example_var(mocker: MockerFixture, valid_env_vars: dict[str, str]) -> None:
    mocker.patch.dict("os.environ", valid_env_vars)

    settings = Settings()

    assert settings.some_example_var == 5


def test_settings_type_coercion_for_integer(mocker: MockerFixture, valid_env_vars: dict[str, str]) -> None:
    env_with_int = {**valid_env_vars, "SOME_EXAMPLE_VAR": "99"}
    mocker.patch.dict("os.environ", env_with_int)

    settings = Settings()

    assert settings.some_example_var == 99
    assert isinstance(settings.some_example_var, int)


def test_settings_invalid_type_for_integer(mocker: MockerFixture, valid_env_vars: dict[str, str]) -> None:
    env_with_invalid = {**valid_env_vars, "SOME_EXAMPLE_VAR": "not-a-number"}
    mocker.patch.dict("os.environ", env_with_invalid)

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("some_example_var",) for error in errors)


def test_settings_secret_str_can_be_retrieved(mocker: MockerFixture, valid_env_vars: dict[str, str]) -> None:
    mocker.patch.dict("os.environ", valid_env_vars)

    settings = Settings()

    assert settings.example_envvar.get_secret_value() == "secret-value-123"


def test_nested_settings_missing_required_field() -> None:
    with pytest.raises(ValidationError) as exc_info:
        NestedSettings()

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("some_nested_envvar",) for error in errors)


def test_settings_with_empty_string_values(
    mocker: MockerFixture,
) -> None:
    mocker.patch.dict(
        "os.environ",
        {"EXAMPLE_ENVVAR": "", "NESTED__SOME_NESTED_ENVVAR": ""},
    )

    settings = Settings()

    assert settings.example_envvar.get_secret_value() == ""
    assert settings.nested.some_nested_envvar == ""
