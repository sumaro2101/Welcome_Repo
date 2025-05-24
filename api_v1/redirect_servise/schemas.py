from pydantic import BaseModel, PositiveInt, Field

from config import settings


class UrlSchema(BaseModel):
    """
    Base Url Schema
    """
    url: str = Field(
        pattern=settings.regex.URL_VALIDATION,
        examples=['/employee?age=10&prof="super"'],
        )


class ViewUrlSchema(UrlSchema):
    """
    View Url Schema
    """
    id: PositiveInt
