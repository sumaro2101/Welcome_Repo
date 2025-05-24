from starlette.exceptions import HTTPException


class UrlNotFoundError(HTTPException):
    """
    Exception ``Url not found``.
    """

    pass


class UrlAlreadyExistsError(HTTPException):
    """
    Exception ``Url already exists``.
    """

    pass
