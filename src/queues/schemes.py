from typing import List, Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class StatusSuccess(BaseModel):
    pass


class EngineV1Params(BaseModel):
    param_1: str | None = None
    param_2: float | None = None
    param_3: bool | None = None

    class Config:
        exclude_none = True


class EngineV2Params(BaseModel):
    param_1: str | None = None
    param_2: float | None = None

    class Config:
        exclude_none = True


class NewQueue(BaseModel):
    engine: str
    engine_v1: EngineV1Params | None = None
    engine_v2: EngineV2Params | None = None

    class Config:
        exclude_none = True


class Task(BaseModel):
    engine: str
    params: EngineV1Params | EngineV2Params
    error: str | None = None


class Tasks(BaseModel):
    tasks: List[Task] | None
