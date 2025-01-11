from dataclasses import dataclass
from enum import Enum

from pydantic_settings import BaseSettings
from typing import List, Tuple


@dataclass(frozen=True)
class PathsConfig:
    TEMPLATES: str = 'templates/'
    STATIC: str = 'static/'


@dataclass(frozen=True)
class URLPathsConfig:
    PREFIX: str = '/api/v1'
    STATIC: str = '/static'
    DOCS: str = '/docs'


@dataclass(frozen=True)
class URLNamesConfig:
    PREFIX: str = '/api/v1/'
    HOMEPAGE: str = 'homepage'
    STATIC: str = 'static'


@dataclass(frozen=True)
class RouterConfig:
    PREFIX: str
    TAGS: Tuple[str]

    @classmethod
    def tags_list(cls) -> List[str | Enum]:
        return [tag for tag in cls.TAGS]


class CORSConfig(BaseSettings):
    ALLOW_ORIGINS: List[str]
    ALLOW_HEADERS: List[str]
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: List[str]


# class UvicornConfig(BaseSettings):
#     HOST: str = '0.0.0.0'
#     PORT: int = 8000
#     LOG_LEVEL: str = 'info'
#     RELOAD: bool = True


# class LinksConfig(BaseSettings):
#     HTTP_PROTOCOL: str
#     DOMAIN: str


class SecurityConfig(BaseSettings):
    SECRET_KEY: str


class UserLoginConfig(BaseSettings):
    TOKEN_EXPIRY_TIME_HOURS: int


cors_config: CORSConfig = CORSConfig()
security_config: SecurityConfig = SecurityConfig()
user_login_config: UserLoginConfig = UserLoginConfig()
