from pydantic import BaseModel


class CustomErrorModel(BaseModel):
    status: bool
    error_code: int
    detail: str | dict[str, str]
