from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi_login import LoginManager

from .config import URLPathsConfig, cors_config, security_config
from .middleware.prometheus_metrics import prometheus_middleware
from .v1.services.metrics import metrics_app

app = FastAPI()

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
    security_config.SECRET_KEY, token_url=URLPathsConfig.PREFIX + "/auth/login"
)

from .v1.endpoints import goods  # noqa: F401, F402, E402
from .v1.endpoints import (bills, categories, login_links, metrics, product,
                           sellers, units, users)

app.mount("/metrics", metrics_app)
