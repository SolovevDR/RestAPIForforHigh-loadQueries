from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.db_user}:{settings.db_pass}@"
    f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
Base = declarative_base()

engine = create_engine(DATABASE_URL, poolclass=NullPool)
Session = sessionmaker(engine)


def get_session() -> Session:
    session = Session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
