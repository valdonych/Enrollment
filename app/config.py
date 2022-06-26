import os
from functools import lru_cache
from typing import Optional, Union

from pydantic import BaseSettings
from starlette.config import Config

getenv = Config('.env')


class GlobalConfig(BaseSettings):
    DESCRIPTION = 'Second stage of backend school'
    DEBUG: bool = False
    TESTING: bool = False
    SERVICE_NAME = 'JustMarkIt'
    PAGE_SIZE: int = getenv('PAGE_SIZE', cast=int, default=5)
    DATABASE_URL = getenv(
        'DATABASE_URL', cast=str, default=os.environ.get('DATABASE_URL')
    )
    ENVIRONMENT: Optional[str] = getenv(
        'ENVIRONMENT', cast=str, default=os.environ.get('ENVIRONMENT')
    )
    SECRET_LOGIN_KEY = getenv(
        'SECRET_LOGIN_KEY',
        cast=str,
        default=os.environ.get('SECRET_LOGIN_KEY', 'bad-key'),
    )


class DevConfig(GlobalConfig):
    DESCRIPTION: str = 'ATTENTION: DevConfig are on'
    DEBUG: bool = True


class TestConfig(GlobalConfig):
    DESCRIPTION: str = 'ATTENTION: TestConfig are on'
    DEBUG: bool = True
    TESTING: bool = True


class FactoryConfig:
    """Returns a config instance depends on the ENV_STATE variable."""

    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> Union[TestConfig, DevConfig]:
        if self.environment == 'TEST':
            return TestConfig()
        return DevConfig()  # pragma: no cover


@lru_cache()
def get_configuration() -> Union[TestConfig, DevConfig]:
    return FactoryConfig(GlobalConfig().ENVIRONMENT)()


config = get_configuration()
