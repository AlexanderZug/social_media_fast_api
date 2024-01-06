import pytest
import os

from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from fastapi.testclient import TestClient

os.environ["ENV_STATE"] = "test"
from db import database  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
async def db() -> Generator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
