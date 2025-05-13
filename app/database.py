from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DB_URL
    params = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.DB_URL
    params = {}

engine = create_async_engine(DATABASE_URL, **params)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
