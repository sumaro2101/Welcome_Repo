from config.dao import BaseDAO
from config.models import RedirectURL


class RedirectServiseDAO(BaseDAO):
    """
    Class DAO for redirect servise
    """
    model = RedirectURL
