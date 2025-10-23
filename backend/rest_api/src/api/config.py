from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

from pydantic_settings import BaseSettings


# @dataclass(frozen=True)
# class RouterConfig:
#     PREFIX: str
#     TAGS: Tuple[str]

#     @classmethod
#     def tags_list(cls) -> List[str | Enum]:
#         return [tag for tag in cls.TAGS]


class CORSConfig(BaseSettings):
    ALLOW_ORIGINS: List[str]
    ALLOW_HEADERS: List[str]
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: List[str]


class MetricsConfig(BaseSettings):
    METRICS_PREFIX: str = "my_app"


class SecurityConfig(BaseSettings):
    SECRET_KEY: str


class UserLoginConfig(BaseSettings):
    TOKEN_EXPIRY_TIME_HOURS: int


class AppConfig(BaseSettings):
    REST_API_APP_NAME: str = "My Application"
    REST_API_STATIC: str = "/static"
    REST_API_DOCS: str = "/docs"
    REST_API_HOST: str
    REST_API_PORT: str
    REST_API_PREFIX: str
    REST_API_LOGIN_LINK_URI: str


cors_config: CORSConfig = CORSConfig()
security_config: SecurityConfig = SecurityConfig()
user_login_config: UserLoginConfig = UserLoginConfig()
metric_config: MetricsConfig = MetricsConfig()
app_config: AppConfig = AppConfig()
