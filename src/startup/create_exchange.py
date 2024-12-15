import aio_pika

from aio_pika import ExchangeType

from rabbit import RABBIT_URL
from config import settings


async def create_queues_and_exchanges():
    connection = await aio_pika.connect_robust(RABBIT_URL)
    async with connection:
        channel = await connection.channel()

        main_exchange = await channel.declare_exchange(
            settings.rmq_queue_exchange,
            ExchangeType.DIRECT,
            durable=True,
        )
        main_queue = await channel.declare_queue(
            settings.rmq_queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": settings.rmq_queue_dead_letter_exchange,
                "x-dead-letter-routing-key": (
                    settings.rmq_queue_routing_key_dead_letter
                ),
            },
        )
        await main_queue.bind(main_exchange, routing_key=settings.rmq_queue_routing_key)

        dlx_exchange = await channel.declare_exchange(
            settings.rmq_queue_dead_letter_exchange,
            ExchangeType.DIRECT,
            durable=True,
        )
        dlx_queue = await channel.declare_queue(
            settings.rmq_queue_dead_letter_name, durable=True
        )
        await dlx_queue.bind(
            dlx_exchange, routing_key=settings.rmq_queue_routing_key_dead_letter
        )


# {'x-dead-letter-exchange': 'dlt-tasks-exchange', 'x-dead-letter-exchange-routing-key': 'dlt-tasks-routing-key'}
# {'x-dead-letter-exchange': 'dlt-tasks-exchange', 'x-dead-letter-exchange-routing-key': 'dlt-tasks-routing-key'}
