from functools import lru_cache
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class PoolSettings(BaseModel):
    size: int = Field(default=5, alias="SIZE")
    max_overflow: int = Field(default=10, alias="MAX_OVERFLOW")
    timeout: int = Field(default=30, alias="TIMEOUT")
    recycle: int = Field(default=3600, alias="RECYCLE")


class DatabaseSettings(BaseModel):
    debug: bool = Field(default=False, alias="DEBUG")
    driver: str = Field(default="postgresql+psycopg", alias="DRIVER")
    host: str = Field(default="localhost", alias="HOST")
    port: int = Field(default=5432, alias="PORT")
    name: str = Field(default="postgres", alias="NAME")
    user: str = Field(default="postgres", alias="USER")
    password: str = Field(alias="PASSWORD")
    pool: PoolSettings = Field(alias="POOL")


class LogSettings(BaseModel):
    level: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        alias="LEVEL"
    )
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        alias="FORMAT"
    )
    date_format: str = Field(default="%Y-%m-%d %H:%M:%S", alias="DATE_FORMAT")
    log_to_file: bool = Field(default=False, alias="LOG_TO_FILE")
    log_file_path: Optional[str] = Field(default=None, alias="LOG_FILE_PATH")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        case_sensitive=True,
        extra="allow",
    )

    app_name: str = Field(default="Minha API", alias="APP_NAME")
    admin_email: str = Field(alias="ADMIN_EMAIL")
    database: DatabaseSettings = Field(alias="DATABASE")
    log: LogSettings = Field(alias="LOG")

    @field_validator("admin_email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("email inválido")
        return v.lower()

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

