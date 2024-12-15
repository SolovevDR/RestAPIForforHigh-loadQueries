from typing import List
from uuid import UUID

from sqlalchemy import select, update, or_, and_, func, asc, desc, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exceptions import NotFoundError
from models.models import Results
from results.schemes import Result


async def select_result(
    session: AsyncSession,
    result_uuid: UUID,
) -> bytes:
    query = select(Results.stdout).filter(Results.result_uuid == result_uuid).limit(1)
    result = await session.execute(query)
    result = result.first()
    if result:
        return result.stdout
    else:
        raise NotFoundError


async def select_results(
    session: AsyncSession,
) -> List[Result]:
    query = select(
        Results.result_uuid,
        Results.engine,
        Results.params,
        Results.end_at,
    )
    result = await session.execute(query)
    result = result.all()
    if result:
        return [Result.from_orm(_) for _ in result]
    return []
