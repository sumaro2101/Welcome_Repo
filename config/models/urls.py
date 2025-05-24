from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

from .base import Base


class RedirectURL(Base):
    """
    Model RedirectUrl
    """
    url: Mapped[str] = mapped_column(String(256), index=True)
