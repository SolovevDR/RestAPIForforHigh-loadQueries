import json
import subprocess
import logging
import random
import time
from typing import TYPE_CHECKING

from crud import insert_result

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

from config import settings
from rabbit import get_connection, create_channel
from utils import create_engines_params, select_params, generate_queue_uuid

DEFAULT_LOG_FORMAT = "%(module)s:%(lineno)d %(levelname)-6s - %(message)s"


def configure_logging(
    level: int = logging.INFO,
    pika_log_level: int = logging.WARNING,
) -> None:
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=DEFAULT_LOG_FORMAT,
    )
    logging.getLogger("pika").setLevel(pika_log_level)


def process_new_message(
    ch: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    log.info("[ ] Start processing task")

    params, engine = select_params(body=body)
    command = create_engines_params(params=params, engine=engine)

    if random.randint(1, 100) > 80:
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        time.sleep(1)
        log.info(f"--- Could not process task {params}")
    else:
        result = subprocess.run(command, shell=True, capture_output=True)
        stdout, stderr = result.stdout, result.stderr
        result_uuid = generate_queue_uuid()
        insert_result(
            result_uuid=result_uuid,
            engine=engine,
            stdout=stdout,
            stderr=stderr,
            params=json.dumps(params)
        )
        log.info(f"+++ Finished processing {params}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    log.info(f"[X] Finished processing task")


def consume_messages(ch: "BlockingChannel") -> None:
    log.info(f"[X] Waiting tasks ...")
    ch.basic_consume(
        queue=settings.rmq_queue_name,
        on_message_callback=process_new_message,
    )
    ch.basic_qos(prefetch_count=1)
    ch.start_consuming()


if __name__ == "__main__":
    configure_logging(level=logging.INFO)
    log = logging.getLogger(__name__)
    with get_connection() as connection:
        with connection.channel() as channel:
            create_channel(channel=channel)
            consume_messages(ch=channel)
