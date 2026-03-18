import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest
from httpx import ASGITransport, AsyncClient

from app.database.base import Base
from app.models.wallet import Wallet
from app.main import app
from app.database.session import get_async_session
from app.core.config import TEST_DATABASE_URL


TEST_DATABASE_URL = TEST_DATABASE_URL
test_engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True)
get_test_session = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with test_engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def client():
    async def override_get_db():
        async with get_test_session() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

    await test_engine.dispose()


@pytest.fixture
async def wallet(client):
    wallet = await client.post("/api/v1/wallets/")

    assert wallet.status_code == 200
    wallet_id = wallet.json()["wallet_id"]

    return wallet_id
