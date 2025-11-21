"""Database configuration with SQLAlchemy async engine."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Create async engine
# Create async engine
engine_args = {
    "echo": False,
    "pool_pre_ping": True,
}

if "sqlite" not in str(settings.DATABASE_URL):
    engine_args["pool_size"] = 10
    engine_args["max_overflow"] = 20

engine = create_async_engine(
    str(settings.DATABASE_URL),
    **engine_args,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
