from fastapi import Depends, Response, APIRouter
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from results.crud import select_results, select_result
from results.schemes import AllResults
from results.utils import create_response

router = APIRouter(prefix="/api/v1/result", tags=["result"])


@router.get("/", response_model=AllResults)
async def select_all_results(session: AsyncSession = Depends(get_async_session)):
    result = await select_results(session=session)
    return AllResults(all_results=result)


@router.get("/{result_uuid}")
async def select_tasks(
    result_uuid: str,
    session: AsyncSession = Depends(get_async_session),
):
    stdout = await select_result(session=session, result_uuid=result_uuid)
    response = await create_response(stdout=stdout)
    return response
