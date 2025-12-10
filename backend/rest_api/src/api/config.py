from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple
from pydantic import BaseModel
from pydantic_settings import BaseSettings


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
    TOKEN_EXPIRY_TIME_HOURS: int = 1


class AppConfig(BaseSettings):
    REST_API_APP_NAME: str = "My Application"
    REST_API_STATIC: str = "/static"
    REST_API_DOCS: str = "/docs"
    REST_API_HOST: str
    REST_API_PORT: str
    REST_API_PREFIX: str
    REST_API_LOGIN_LINK_URI: str


class RedisDB(BaseModel):
    cache: int = 0


class RedisConfig(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    db: RedisDB = RedisDB()


class CacheNamespace(Enum):
    PRODUCTS = "products"
    CATEGORIES = "categories"
    SELLERS = "sellers"
    UNITS = "units"
    GOODS = "goods"
    USERS = "users"
    BILLS = "bills"


class CacheConfig(BaseModel):
    cache_ttl_seconds: int = 300
    prefix: str = "qr_bill_app_cache"
    namespace: CacheNamespace = CacheNamespace.PRODUCTS


cors_config: CORSConfig = CORSConfig()
security_config: SecurityConfig = SecurityConfig()
user_login_config: UserLoginConfig = UserLoginConfig()
metric_config: MetricsConfig = MetricsConfig()
app_config: AppConfig = AppConfig()
redis_config: RedisConfig = RedisConfig()
redis_db: RedisDB = RedisDB()
cache_config: CacheConfig = CacheConfig()
