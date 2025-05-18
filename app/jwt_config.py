from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT CONFIG
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # DB CONFIG
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
