import pytest
from api.security import get_user


@pytest.mark.asyncio
async def test_get_user(registered_user: dict):
    user = await get_user(registered_user["email"])
    assert user["email"] == registered_user["email"]
    assert user["id"] == registered_user["id"]
