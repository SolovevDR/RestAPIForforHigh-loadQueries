import hashlib
import json
from time import time_ns
from uuid import UUID

from crud import select_result_uuid
from enums import Engines
from schemes import EngineV1Params, EngineV2Params


def select_params(body: bytes) -> tuple[dict, str]:
    params = json.loads(body.decode())
    engine_name = params.pop("engine", None)

    return params, engine_name


def create_engines_params(params: dict, engine: str) -> list[str]:
    if engine == Engines.ENGINE_V1.value:
        params = EngineV1Params.model_validate(params)
    elif engine == Engines.ENGINE_V2.value:
        params = EngineV2Params.model_validate(params)

    params = params.model_dump(exclude_none=True)
    params = [params[key] for key in params.keys()]
    command = ["python", f"engines/engine_{engine}/start.py"]
    for param in params:
        command.extend(param.split(" "))
    return command


def generate_queue_uuid() -> UUID:
    while True:
        result_uuid = hashlib.md5(f"{time_ns():x}".encode()).hexdigest()
        result = select_result_uuid(result_uuid=result_uuid)
        result = result.first()
        if not result:
            return result_uuid
