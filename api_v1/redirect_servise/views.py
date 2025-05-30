from typing import Annotated

from fastapi import APIRouter, status, Depends, Path
from fastapi_cache.decorator import cache
from fastapi.responses import RedirectResponse

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from config import db_connection
from config import settings
from api_v1.error_models import CustomErrorModel
from .schemas import UrlSchema, ViewUrlSchema
from .dao import RedirectServiseDAO
from .exceptions import (
    UrlNotFoundError,
    UrlAlreadyExistsError,
    )
from .common import ErrorCode


router = APIRouter(
    prefix='/urls',
    tags=['URL'],
)


@router.get(path='',
            name='urls:list',
            description='Getting `list` of short urls.',
            response_model=list[ViewUrlSchema],
            )
@cache(expire=settings.MAX_CACHE_EXPIRE)
async def get_list_urls(session: AsyncSession = Depends(db_connection.session_geter)):
    return await RedirectServiseDAO.find_all_items_by_args(session=session)


@router.post(path='',
             name='urls:create',
             description='`Create` new short url.',
             response_model=ViewUrlSchema,
             responses={
                 status.HTTP_422_UNPROCESSABLE_ENTITY: {
                     'model': CustomErrorModel,
                     'content': {
                         'application/json': {
                             'examples': {
                                 ErrorCode.URL_ALREADY_EXISTS_ERROR: {
                                     'summary': 'Url already exists',
                                     'value': {
                                         'status': False,
                                         'error_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                                         'detail': ErrorCode.URL_ALREADY_EXISTS_ERROR,
                                     }
                                 }
                             },
                         }
                     }
                 }
             },
             status_code=status.HTTP_201_CREATED,
             )
async def create_short_url(short_url: UrlSchema,
                           session: AsyncSession = Depends(db_connection.session_geter)):
    logger.info(f'POST method get data {short_url}')
    try:
        url = await RedirectServiseDAO.add(
            session=session,
            url=short_url.url,
        )
    except IntegrityError:
        raise UrlAlreadyExistsError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail=ErrorCode.URL_ALREADY_EXISTS_ERROR,
                                    )
    return url


@router.get(path='/{url_id}',
            name='urls:get',
            description='`Get` and `Redirect Temporary` from short `url`.',
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'model': CustomErrorModel,
                    'content': {
                        'application/json': {
                            'examples': {
                                ErrorCode.URL_NOT_FOUND_ERROR: {
                                    'summary': 'Url with this `id` not `contains` in `Data Base`',
                                    'value': {
                                        'status': False,
                                        'error_code': status.HTTP_404_NOT_FOUND,
                                        'detail': ErrorCode.URL_NOT_FOUND_ERROR,
                                        }
                                    }
                                }
                            },
                        }
                    }
                },
            response_class=RedirectResponse,
            )
@cache(expire=settings.MAX_CACHE_EXPIRE)
async def get_and_redirect_url(url_id: Annotated[int,
                                                 Path(title='Id short url',
                                                      ge=1,
                                                      examples=[23],
                                                      )],
                               session: AsyncSession = Depends(db_connection.session_geter),
                               ):
    url = await RedirectServiseDAO.find_item_by_args(
        session=session,
        id=url_id,
    )
    if not url:
        raise UrlNotFoundError(status_code=status.HTTP_404_NOT_FOUND,
                               detail=ErrorCode.URL_NOT_FOUND_ERROR,
                               )
    return url.url


@router.delete(path='/{url_id}',
               name='urls:delete',
               description='`Delete` exists short url by `id`.',
               status_code=status.HTTP_204_NO_CONTENT,
               responses={
                   status.HTTP_404_NOT_FOUND: {
                       'model': CustomErrorModel,
                       'content': {
                           'application/json': {
                               'examples': {
                                   ErrorCode.URL_NOT_FOUND_ERROR: {
                                       'summary': 'Url with this `id` not `contains` in `Data Base`',
                                       'value': {
                                           'status': False,
                                           'error_code': status.HTTP_404_NOT_FOUND,
                                           'detail': ErrorCode.URL_NOT_FOUND_ERROR,
                                       }
                                   }
                               }
                           },
                       }
                   }
               },
               )
async def delete_short_url(url_id: Annotated[int,
                                             Path(title='Id short url',
                                                  ge=1,
                                                  examples=[23],
                                                  )],
                           session: AsyncSession = Depends(db_connection.session_geter),
                           ):
    url = await RedirectServiseDAO.find_item_by_args(
        session=session,
        id=url_id,
    )
    if not url:
        raise UrlNotFoundError(status_code=status.HTTP_404_NOT_FOUND,
                               detail=ErrorCode.URL_NOT_FOUND_ERROR,
                               )
    return await RedirectServiseDAO.delete(
        session=session,
        instance=url,
        )
