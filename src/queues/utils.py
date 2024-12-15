import hashlib
import json
from time import time_ns
from uuid import UUID

import aio_pika
from aio_pika import Channel

from enums import Engines
from config import settings
from exceptions.exceptions import ExchangeNotFound
from queues.schemes import NewQueue, EngineV1Params, EngineV2Params, Task
from rabbit import RABBIT_URL


async def select_engine_params(
    queue_value: NewQueue,
) -> str:
    params_str = None
    if queue_value.engine == Engines.ENGINE_V1.value:
        params_str = queue_value.engine_v1.model_dump(exclude_none=True)
    elif queue_value.engine == Engines.ENGINE_V2.value:
        params_str = queue_value.engine_v2.model_dump(exclude_none=True)
    return json.dumps(
        {
            **params_str,
            "engine": queue_value.engine,
        }
    )


async def validate_engine_params(tasks_params: dict) -> Task:
    engine_name = tasks_params.pop("engine", None)
    error = tasks_params.pop("error", None)
    tasks_params = json.dumps(tasks_params)

    params = None

    if engine_name == Engines.ENGINE_V1.value:
        params = EngineV1Params.model_validate_json(tasks_params)
    elif engine_name == Engines.ENGINE_V2.value:
        params = EngineV2Params.model_validate_json(tasks_params)

    return Task(engine=engine_name, params=params, error=error)


async def send_message(channel: Channel, task: str):
    exchange = await channel.get_exchange(settings.rmq_queue_exchange)
    if exchange is None:
        raise ExchangeNotFound

    await exchange.publish(
        aio_pika.Message(body=task.encode()), routing_key=settings.rmq_queue_routing_key
    )


async def get_message(
    channel: Channel,
    prefetch_count: int = 1,
    is_dlt: bool = False,
    is_delete: bool = True,
):
    await channel.set_qos(prefetch_count=prefetch_count)
    queue = await channel.get_queue(
        settings.rmq_queue_dead_letter_name if is_dlt else settings.rmq_queue_name
    )

    all_messages = queue.declaration_result.message_count
    tasks = []
    message_count = 0
    if all_messages != 0:
        async with queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                _temp = json.loads(message.body.decode())
                tasks.append(await validate_engine_params(tasks_params=_temp))
                if is_delete:
                    await message.ack()
                message_count += 1
                if message_count >= prefetch_count or all_messages - message_count == 0:
                    break
        return tasks
