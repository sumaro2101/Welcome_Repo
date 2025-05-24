import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_short_url(client: AsyncClient, url_data):
    response = await client.post(
        'urls',
        json=url_data,
    )
    assert response.status_code == 201
    assert response.json()['url'] == '/path/some/path'


@pytest.mark.asyncio
async def test_create_unique_short_url(client: AsyncClient, url_data):
    response = await client.post(
        'urls',
        json=url_data,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_wrong_short_url(client: AsyncClient, url_wrong_data):
    response = await client.post(
        'urls',
        json=url_wrong_data,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_script_url(client: AsyncClient, url_sctipt_data):
    response = await client.post(
        'urls',
        json=url_sctipt_data,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_redirect(client: AsyncClient):
    response = await client.get(
        'urls',
        )
    id_path = response.json()[0]['id']
    response = await client.get(
        f'urls/{id_path}',
        )
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_delete_url(client: AsyncClient):
    response = await client.get(
        'urls',
        )
    id_path = response.json()[0]['id']
    response = await client.delete(
        f'urls/{id_path}',
        )
    assert response.status_code == 204
