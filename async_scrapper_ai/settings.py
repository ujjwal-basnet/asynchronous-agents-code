from typing import Annotated, Set
from pydantic import Field, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Centralized configuration management using Pydantic v2.
    Automatically reads environment variables, validates types,
    enforces required fields, and applies defaults where specified.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",  # prevent accidental or mistyped env vars
    )

    # Server
    port: Annotated[int, Field(default=8000)]

    # Security
    app_secret: Annotated[str, Field(min_length=20)]

    # Database
    pg_dsn: Annotated[
        PostgresDsn,
        Field(
            alias="DATABASE_URL",
            default="postgresql://scraper_user:scrap123@localhost:5432/scraping_db"
        )]

    # CORS
    cors_whitelist_domains: Annotated[
        Set[HttpUrl],
        Field(
            alias="CORS_WHITELIST",
            default={"http://localhost:3000"}
        )
    ]


# Singleton instance
settings = AppSettings()


if __name__ == "__main__":
    # Dump all validated settings as a dictionary
    print(settings.model_dump())
