import pytest
import os

from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from fastapi.testclient import TestClient

os.environ["ENV_STATE"] = "test"
from api.db import database, user_table  # noqa: E402
from api.main import app  # noqa: E402


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


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.com", "password": "1234"}

    await async_client.post("/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    result = await database.fetch_one(query)
    user_details["id"] = result["id"]

    return user_details
