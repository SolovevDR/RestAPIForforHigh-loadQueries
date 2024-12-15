from typing import List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Result(BaseModel):
    result_uuid: UUID | None
    engine: str | None
    params: str | None
    end_at: datetime | None

    class Config:
        from_attributes = True


class AllResults(BaseModel):
    all_results: List[Result]

    class Config:
        from_attributes = True
