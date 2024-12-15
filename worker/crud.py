from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from models import Results
from database import get_session


def insert_result(
    result_uuid: UUID,
    engine: str,
    stdout: bytes,
    stderr: bytes,
    params: str,
) -> None:
    end_time = datetime.utcnow()
    session = next(get_session())
    query = Results(
        result_uuid=result_uuid,
        stdout=stdout,
        stderr=stderr,
        params=params,
        engine=engine,
        end_at=end_time
    )
    session.add(query)
    session.commit()


def select_result_uuid(result_uuid: UUID) -> UUID:
    session = next(get_session())
    query = select(Results.result_uuid).filter(Results.result_uuid == result_uuid).limit(1)
    result = session.execute(query)
    return result
