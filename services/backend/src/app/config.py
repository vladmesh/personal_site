"""Application configuration using pydantic-settings."""

import json
from typing import Annotated, Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Database
    DATABASE_URL: str

    # Project
    PROJECT_NAME: str = "Personal Site API"
    ENVIRONMENT: str = "development"

    # API
    API_V1_STR: str = "/api/v1"

    # CORS
    # NoDecode: pydantic-settings otherwise json.loads() the raw env string before our
    # validator runs, which rejects plain comma-separated values outright.
    BACKEND_CORS_ORIGINS: Annotated[list[str], NoDecode] = [
        "http://localhost",
        "http://localhost:4321",
    ]

    # Admin
    ADMIN_USERNAME: str = "admin"
    # PBKDF2 hash, not a plaintext password. Generate with:
    #   python -m app.security '<your password>'
    ADMIN_PASSWORD_HASH: str
    ADMIN_SECRET_KEY: str

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS origins from a JSON array string, a comma-separated string, or a list."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            stripped = v.strip()
            if stripped.startswith("["):
                try:
                    parsed = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"BACKEND_CORS_ORIGINS is not valid JSON: {v!r}") from exc
                if not isinstance(parsed, list) or not all(
                    isinstance(origin, str) for origin in parsed
                ):
                    raise ValueError(
                        f"BACKEND_CORS_ORIGINS JSON array must contain only strings: {v!r}"
                    )
                return [origin.strip() for origin in parsed]
            origins = [origin.strip() for origin in stripped.split(",") if origin.strip()]
            if not origins:
                raise ValueError(f"BACKEND_CORS_ORIGINS has no valid origins: {v!r}")
            return origins
        raise ValueError(f"BACKEND_CORS_ORIGINS must be a string or list, got {type(v)!r}")


settings = Settings()  # type: ignore[call-arg]
