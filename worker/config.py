from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")
    db_port: str = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")

    rmq_host: str = Field(..., env="RMQ_HOST")
    rmq_port: int = Field(..., env="RMQ_PORT")
    rmq_user: str = Field(..., env="RMQ_USER")
    rmq_password: str = Field(..., env="RMQ_PASSWORD")

    rmq_queue_exchange: str = Field(..., env="RMQ_QUEUE_EXCHANGE")
    rmq_queue_routing_key: str = Field(..., env="RMQ_QUEUE_ROUTING_KEY")
    rmq_queue_name: str = Field(..., env="RMQ_QUEUE_NAME")
    rmq_queue_dead_letter_exchange: str = Field(..., env="RMQ_QUEUE_DEAD_LETTER_EXCHANGE")
    rmq_queue_routing_key_dead_letter: str = Field(
        ..., env="RMQ_QUEUE_ROUTING_KEY_DEAD_LETTER"
    )
    rmq_queue_dead_letter_name: str = Field(..., env="RMQ_QUEUE_DEAD_LETTER_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
