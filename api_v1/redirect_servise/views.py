from fastapi import APIRouter, status, Depends
from fastapi_cache.decorator import cache
from fastapi.responses import RedirectResponse

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession

from config import db_connection
from config import settings
from .schemas import UrlSchema, ViewUrlSchema
from .dao import RedirectServiseDAO


router = APIRouter(
    prefix='/urls',
    tags=['URL'],
)


@router.get(path='',
            name='urls:list',
            response_model=list[ViewUrlSchema],
            )
@cache(expire=settings.MAX_CACHE_EXPIRE)
async def get_list_urls(session: AsyncSession = Depends(db_connection.session_geter)):
    return await RedirectServiseDAO.find_all_items_by_args(session=session)


@router.post(path='',
             name='urls:create',
             response_model=ViewUrlSchema,
             status_code=status.HTTP_202_ACCEPTED,
             )
async def create_short_url(short_url: UrlSchema,
                           session: AsyncSession = Depends(db_connection.session_geter)):
    logger.info(f'POST method get data {short_url}')
    return await RedirectServiseDAO.add(
        session=session,
        url=short_url.url,
    )
