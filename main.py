from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from api_v1 import register_routers
from app_includes import (
    register_errors,
    register_middlewares,
    )
from config import settings


def start_app() -> FastAPI:
    """
    Создание приложения со всеми настройками
    """
    app = FastAPI(lifespan=lifespan)
    register_routers(app=app)
    register_errors(app=app)
    register_middlewares(app=app)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.redis.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield


app = start_app()
