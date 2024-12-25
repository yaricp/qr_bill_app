from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.orm import clear_mappers

from fastapi import FastAPI
# from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
# from starlette import status

from backend.config import (
    cors_config, URLPathsConfig, URLNamesConfig, 
)
from backend.infra.database.connection import DATABASE_URL
from backend.infra.database.metadata import metadata

# from backend.core.infra.outside_broker.connection import (
#     KAFKA_TOPICS, KAFKA_SERVERS
# )

from backend.api.v1.routers import api_router
# from backend.infra.orm import start_mappers

# from backend.partner.infra.adapters.kafka_adapter import (
#     create_topics
# )


# @asynccontextmanager
# async def lifespan(_app: FastAPI) -> AsyncGenerator:
#     """
#     Runs events before application startup and after application shutdown.
#     """

#     # Startup events:
#     engine: AsyncEngine = create_async_engine(DATABASE_URL)
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.create_all)

#     start_mappers()
#     # topics=KAFKA_TOPICS, kafka_servers=KAFKA_SERVERS
#     # create_topics()

#     yield

#     # Shutdown events:
#     clear_mappers()

# lifespan=lifespan

app = FastAPI()

# Middlewares:
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ALLOW_ORIGINS,
    allow_credentials=cors_config.ALLOW_CREDENTIALS,
    allow_methods=cors_config.ALLOW_METHODS,
    allow_headers=cors_config.ALLOW_HEADERS,
)

# Routers:
app.include_router(api_router)
