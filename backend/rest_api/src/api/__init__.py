# from sqlalchemy.orm import clear_mappers

from fastapi import FastAPI
# from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager

from ..infra.database.connection import DATABASE_URL
from ..infra.database.metadata import metadata

from .config import (
    cors_config, url_peths_config, security_config 
)
from .v1.routers import api_router


app = FastAPI()

# app.mount("/static", StaticFiles(directory="/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"SECRET_KEY: {security_config.SECRET_KEY}")

manager = LoginManager(
    security_config.SECRET_KEY,
    token_url=url_peths_config.PREFIX + '/auth/login'
)
app.include_router(api_router)
