from enum import StrEnum

from pydantic import BaseModel, PostgresDsn, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.metadata import metadata


class Environments(StrEnum):
    LOCAL = "LOCAL"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class LogLevels(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class AppSettings(BaseModel):
    """Application settings with metadata loaded from package configuration.

    This class represents core application settings that are automatically populated
    from the package's metadata (currently from pyproject.toml and not installed package metadata)
    with fallback default values.

    Attributes:
        NAME (str): The formal name of the application/service.
            Default: Loaded from package metadata (metadata.name)
        VERSION (str): Current version of the application in semver format.
            Default: Loaded from package metadata (metadata.version)
        DESCRIPTION (str): Brief description of the application's purpose.
            Default: Loaded from package metadata (metadata.description)
        CONTACT_NAME (str): Primary contact person's name for the application.
            Default: First author's name from metadata or "Mohamad Amin Jafari"
        CONTACT_EMAIL (str): Primary contact email for the application.
            Default: First author's email from metadata or "mhmdamin.jafari@gmail.com"
        CONTACT_URL (str | None): Optional URL for application support/contact.
            Default: None

    Note:
        - All fields automatically load values from package metadata when available
        - Contact fields fall back to developer defaults when metadata isn't available
        - CONTACT_URL must be explicitly set as it's not typically in package metadata
    """

    NAME: str = metadata.name
    VERSION: str = metadata.version
    DESCRIPTION: str = metadata.description
    CONTACT_NAME: str = metadata.authors[0].name or "Mohamad Amin Jafari"
    CONTACT_EMAIL: str = metadata.authors[0].email or "mhmdamin.jafari@gmail.com"
    CONTACT_URL: str | None = None


class PostgresSettings(BaseModel):
    """Configuration settings for Postgres database connections.

    Attributes:
        USER (str): Database username. Default: "postgres"
        PASSWORD (str): Database password. Default: "postgres"
        HOST (str): Database host. Default: "localhost"
        PORT (int): Database port. Default: 5432
        DB (str): Database name. Default: "postgres"
        SYNC_SCHEMA (str): Schema for synchronous connections. Default: "postgresql"
        ASYNC_SCHEMA (str): Schema for asynchronous connections. Default: "postgresql+asyncpg"

    Computed Fields:
        uri: Basic connection URI without schema
        sync_dsn: Complete synchronous connection DSN
        async_dsn: Complete asynchronous connection DSN
    """

    USER: str = "postgres"
    PASSWORD: str = "postgres"
    HOST: str = "localhost"
    PORT: int = 5432
    DB: str = "postgres"
    SYNC_SCHEMA: str = "postgresql"  # Used for testing
    ASYNC_SCHEMA: str = "postgresql+asyncpg"

    @computed_field
    @property
    def uri(self) -> str:
        """Generate the base connection URI without schema.

        Format: {USER}:{PASSWORD}@{HOST}:{PORT}/{DB}
        """
        return f"{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    @computed_field
    @property
    def sync_dsn(self) -> PostgresDsn:
        """Generate complete synchronous Postgres connection DSN."""
        return PostgresDsn(f"{self.SYNC_SCHEMA}://{self.uri}")

    @computed_field
    @property
    def async_dsn(self) -> PostgresDsn:
        """Generate complete asynchronous Postgres connection DSN."""
        return PostgresDsn(f"{self.ASYNC_SCHEMA}://{self.uri}")


class Settings(BaseSettings):
    """Root application settings with environment configuration.

    Combines all configuration sections and handles environment variable loading.

    Configuration:
        - Loads from .env file
        - Supports nested environment variables with '__' delimiter
        - Allows partial updates for nested models
        - Maintains case sensitivity

    Attributes:
        APP (AppSettings): Application metadata settings
        ENVIRONMENT (Environments): Current deployment environment
        LOG_LEVEL (LogLevels): Application logging level
        POSTGRES (PostgresSettings): Database configuration

    Validators:
        to_uppercase: Ensures ENVIRONMENT and LOG_LEVEL values are uppercase
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", nested_model_default_partial_update=True, case_sensitive=True
    )

    ENVIRONMENT: Environments = Environments.LOCAL
    LOG_LEVEL: LogLevels = LogLevels.INFO
    APP: AppSettings = AppSettings()
    POSTGRES: PostgresSettings = PostgresSettings()

    @field_validator("ENVIRONMENT", "LOG_LEVEL", mode="before", check_fields=False)
    def to_uppercase(cls, value: str) -> str:
        return value.upper()


settings = Settings()
"""Pre-configured settings instance loaded at module level.

This instance is created when the module is imported and contains all application settings
loaded from environment variables and .env file, with defaults where not specified.
"""
