from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings




DATABASE_PARAMS: dict[str, int] = {
    'pool_size': settings.POOL_SIZE,
    'max_overflow': settings.MAX_OVERFLOW,
    'pool_timeout': settings.POOL_TIMEOUT
}

engine = create_async_engine(settings.database_url, **DATABASE_PARAMS)


async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

