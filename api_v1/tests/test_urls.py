import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test(client: AsyncClient, user_test_data):
    ...
