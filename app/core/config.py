import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
