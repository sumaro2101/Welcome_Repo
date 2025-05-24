from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from starlette.config import Config


base_dir = Path(__file__).resolve().parent.parent
log_dir = base_dir.joinpath('logs')


config = Config('.env')


class AlembicSettings(BaseModel):
    """
    Настройки Alembic
    """
    CONFIG_PATH: Path = Path('alembic.ini')
    MIGRATION_PATH: Path = Path('async_alembic')


class TestDBSettings(BaseModel):
    """
    Настройки тестовой базы данных
    """
    _engine: str = config('TEST_DB_ENGINE')
    _owner: str = config('TEST_DB_USER')
    _password: str = config('TEST_DB_PASSWORD')
    _name: str = config('TEST_DB_HOST')
    _db_name: str = config('TEST_DB_NAME')
    url: str = f'{_engine}://{_owner}:{_password}@{_name}/{_db_name}'


class DBSettings(BaseModel):
    """
    Настройки DataBase
    """
    _engine: str = config('DB_ENGINE')
    _owner: str = config('DB_USER')
    _password: str = config('DB_PASSWORD')
    _name: str = config('DB_HOST')
    _db_name: str = config('DB_NAME')
    url: str = f'{_engine}://{_owner}:{_password}@{_name}/{_db_name}'


class RedisSettings(BaseModel):
    """
    Настройки Redis
    """
    REDIS_HOST: str = config('REDIS_HOST')
    REDIS_PORT: str = config('REDIS_PORT')
    redis_url: str = ('redis://' +
                      REDIS_HOST)


class Regex(BaseModel):
    """
    Settings for regular
    """
    URL_VALIDATION: str = r"^\/[\/\.a-zA-Z0-9\-?&='\"]+$"


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra='ignore',
    )
    db: DBSettings = DBSettings()
    test_db: TestDBSettings = TestDBSettings()
    redis: RedisSettings = RedisSettings()
    alembic: AlembicSettings = AlembicSettings()
    regex: Regex = Regex()
    debug: bool = bool(int(config('DEBUG')))
    MAX_CACHE_EXPIRE: int = 60
    API_PREFIX: str = '/api/v1'
    BASE_DIR: Path = base_dir
    LOG_DIR: Path = log_dir
    CURRENT_ORIGIN: str = config('CURRENT_ORIGIN')


settings = Settings()
