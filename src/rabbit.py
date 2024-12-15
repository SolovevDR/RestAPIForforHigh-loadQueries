from typing import AsyncGenerator

import aio_pika

from config import settings

RABBIT_URL = (
    f"amqp://{settings.rmq_user}:{settings.rmq_password}"
    f"@{settings.rmq_host}:{settings.rmq_port}/"
)


async def get_async_chanel() -> AsyncGenerator[aio_pika.Channel, None]:
    connection = await aio_pika.connect_robust(RABBIT_URL)
    async with connection:
        try:
            channel = await connection.channel()
            yield channel
        finally:
            await channel.close()
