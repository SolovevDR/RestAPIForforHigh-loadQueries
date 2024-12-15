from typing import TYPE_CHECKING

import pika
if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


from config import settings


connection_params = pika.ConnectionParameters(
    host=settings.rmq_host,
    port=settings.rmq_port,
    credentials=pika.PlainCredentials(
        username=settings.rmq_user,
        password=settings.rmq_password
    ),
)


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(
        parameters=connection_params,
    )


def create_channel(channel: "BlockingChannel" = None):
    channel.exchange_declare(
        exchange=settings.rmq_queue_exchange,
        exchange_type="direct",
        durable=True,
    )
    channel.queue_declare(
        queue=settings.rmq_queue_name,
        durable=True,
        arguments={
            "x-dead-letter-exchange": settings.rmq_queue_dead_letter_exchange,
            "x-dead-letter-routing-key": (
                settings.rmq_queue_routing_key_dead_letter
            ),
        },
    )
    channel.queue_bind(
        queue=settings.rmq_queue_name,
        exchange=settings.rmq_queue_exchange,
        routing_key=settings.rmq_queue_routing_key,
    )

    channel.exchange_declare(
        exchange=settings.rmq_queue_dead_letter_exchange,
        exchange_type="direct",
        durable=True,
    )
    channel.queue_declare(
        queue=settings.rmq_queue_dead_letter_name,
        durable=True,
    )
    channel.queue_bind(
        queue=settings.rmq_queue_dead_letter_name,
        exchange=settings.rmq_queue_dead_letter_exchange,
        routing_key=settings.rmq_queue_routing_key_dead_letter,
    )

