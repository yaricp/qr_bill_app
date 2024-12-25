from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.orm import clear_mappers

from fastapi import FastAPI
# from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager

from backend.config import (
    cors_config, URLPathsConfig, URLNamesConfig, 
)
from backend.infra.database.connection import DATABASE_URL
from backend.infra.database.metadata import metadata


app = FastAPI()
        
app.mount("/static", StaticFiles(directory="/static"), name="static")
        
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = LoginManager(SECRET_KEY, token_url=API_PREFIX + '/auth/login')
app.include_router(api_router)
