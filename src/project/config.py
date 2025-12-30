from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class NestedSettings(BaseModel):
    """Nested configuration settings.

    Environment variables use double underscore delimiter (e.g., NESTED__SOME_NESTED_ENVVAR).
    """

    some_nested_envvar: str = Field(..., description="Example of nested settings")


class Settings(BaseSettings):
    """Application configuration settings.

    Loads configuration from environment variables and .env file.
    Supports nested settings with double underscore delimiter.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    some_example_var: int = Field(5, description="Some value")
    example_envvar: SecretStr = Field(..., description="Example of secret envvar")
    nested: NestedSettings = Field(default_factory=NestedSettings, description="Nested env vars")
