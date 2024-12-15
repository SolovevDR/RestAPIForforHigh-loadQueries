from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")
    db_port: str = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
