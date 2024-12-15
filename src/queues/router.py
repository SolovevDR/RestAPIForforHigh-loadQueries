from fastapi import Depends, Response, APIRouter
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from queues.schemes import NewQueue, StatusSuccess, Tasks
from queues.utils import select_engine_params, send_message, get_message
from rabbit import get_async_chanel

router = APIRouter(prefix="/api/v1/queue", tags=["queue"])


@router.post("/", response_model=StatusSuccess)
async def add_tasks(
    queue_value: NewQueue,
    chanel: AsyncSession = Depends(get_async_chanel),
):
    param_str = await select_engine_params(queue_value=queue_value)
    await send_message(channel=chanel, task=param_str)
    return StatusSuccess()


@router.get("/{number_queues}", response_model=Tasks)
async def select_tasks(
    number_queues: int,
    is_dlt: bool = False,
    is_delete: bool = False,
    chanel: AsyncSession = Depends(get_async_chanel),
):
    tasks = await get_message(
        channel=chanel, prefetch_count=number_queues, is_dlt=is_dlt, is_delete=is_delete
    )
    return Tasks(tasks=tasks if tasks is not None else None)
