

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_username: str = "postgres"
    database_password: str = "0991"
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_name: str = "fastapi"
    secret_key: str = "09d4e4f6c3b5a7e8f1d2c3b4a5e6f70809101112131415161718191a1b1c1d1e"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()