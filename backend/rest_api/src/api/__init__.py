from collections.abc import AsyncIterator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
from fastapi.routing import APIRoute
from fastapi_login import LoginManager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis  import RedisBackend
from redis import asyncio as aioredis

from src.api.config import (
    app_config, cors_config, security_config, cache_config
)
from src.api.redis import redis_client, QRRedisBackend
from src.api.middleware.prometheus_metrics import prometheus_middleware
from src.api.v1.services.metrics import metrics_app


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(
        RedisBackend(redis_client),
        prefix=cache_config.prefix
    )
    yield


app = FastAPI(lifespan=lifespan)

# app.mount("/static", StaticFiles(directory="/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(prometheus_middleware)

print(f"SECRET_KEY: {security_config.SECRET_KEY}")

app.router.route_class = APIRoute

manager = LoginManager(
    security_config.SECRET_KEY, token_url=app_config.REST_API_PREFIX + "/auth/login"
)

from src.api.v1.endpoints import goods  # noqa: F401, F402, E402
from src.api.v1.endpoints import (bills, categories, login_links, metrics,
                                  product, sellers, units, users)

app.mount("/metrics", metrics_app)
