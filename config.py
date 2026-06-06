from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseModel):
    driver: str = Field(default="postgresql", alias="DRIVER")
    host: str = Field(default="localhost", alias="HOST")
    port: int = Field(default=5432, alias="PORT")
    name: str = Field(default="postgres", alias="NAME")
    user: str = Field(default="postgres", alias="USER")
    password: str = Field(alias="PASSWORD")


class LogSettings(BaseModel):
    level: str = Field(default="INFO", alias="LEVEL")
    app_name: str = Field(default="tenantforge", alias="APP_NAME")


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


settings = Settings()
