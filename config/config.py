from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from starlette.config import Config


base_dir = Path(__file__).resolve().parent.parent
log_dir = base_dir.joinpath('logs')


config = Config('.env')


class JWTSettings(BaseModel):
    """
    Настройки JWT токена
    """
    NAME: str = 'jwt'
    SECRET: str = config('SECRET')
    RESET_LIFESPAN_TOKEN_SECONDS: int = 3600
    JWT_PATH: str = '/auth/jwt'


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
    JWT: JWTSettings = JWTSettings()
    debug: bool = bool(int(config('DEBUG')))
    API_PREFIX: str = '/api/v1'
    BASE_DIR: Path = base_dir
    LOG_DIR: Path = log_dir
    CURRENT_ORIGIN: str = config('CURRENT_ORIGIN')


settings = Settings()
