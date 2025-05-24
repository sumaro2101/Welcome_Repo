from starlette.exceptions import HTTPException


class UrlNotFoundError(HTTPException):
    """
    Exception ``Url not found``
    """

    pass
