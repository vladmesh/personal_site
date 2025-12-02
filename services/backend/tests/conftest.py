import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

# Set default env vars for unit testing
if "TEST_DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
if "ADMIN_PASSWORD" not in os.environ:
    os.environ["ADMIN_PASSWORD"] = "test"
if "ADMIN_SECRET_KEY" not in os.environ:
    os.environ["ADMIN_SECRET_KEY"] = "testsecretkey"

from app.database import Base, get_db
from app.main import app


# Determine test mode based on pytest markers
def pytest_configure(config):
    """Configure test environment based on markers."""
    config.addinivalue_line("markers", "unit: Unit tests using SQLite")
    config.addinivalue_line("markers", "integration: Integration tests using PostgreSQL")


# SQLite engine for unit tests
@pytest.fixture(scope="function")
async def sqlite_engine():
    """Create SQLite engine for unit tests."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db(request: pytest.FixtureRequest, sqlite_engine) -> AsyncGenerator[AsyncSession, None]:
    """Provide database session based on test marker."""
    # Check if test is marked as integration
    if request.node.get_closest_marker("integration"):
        # Create postgres engine only for integration tests
        database_url = os.environ.get(
            "TEST_DATABASE_URL",
            "postgresql+asyncpg://test_user:test_password@test-db:5432/test_db",
        )
        engine = create_async_engine(database_url, echo=False)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        session_local = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
        async with session_local() as session:
            yield session
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()
    else:
        session_local = async_sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
        async with session_local() as session:
            yield session


@pytest.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide HTTP client for API testing."""

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
