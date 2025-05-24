from fastapi import APIRouter, status, Depends
from fastapi_cache.decorator import cache
from fastapi.responses import RedirectResponse

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
