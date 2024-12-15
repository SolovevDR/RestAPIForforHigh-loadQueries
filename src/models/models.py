from sqlalchemy import Column, String, DateTime, UUID, Text
from sqlalchemy.dialects.postgresql import BYTEA

from database import Base


class Results(Base):
    __tablename__ = "results"

    result_uuid = Column(UUID, primary_key=True)
    stdout = Column(BYTEA, nullable=True)
    stderr = Column(BYTEA, nullable=True)
    params = Column(String, nullable=False)
    engine = Column(Text, nullable=False)
    end_at = Column(DateTime, nullable=False)
