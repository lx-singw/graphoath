from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "GraphOath"
    environment: str = "development"
    database_url: str = Field(
        default="postgresql://graphoath_user:graphoath_secret_key@localhost:5432/graphoath"
    )
    datahub_gms_url: str = Field(default="http://localhost:8080")
    datahub_token: str = Field(default="dev-token")
    jwt_secret_key: str = Field(default="dev-jwt-secret-key-change-in-production")
    jwt_algorithm: str = "HS256"
    access_token_expire_seconds: int = 43200

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
