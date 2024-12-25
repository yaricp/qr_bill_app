from fastapi import APIRouter

from backend.config import URLPathsConfig

from backend.partner.api.v1.endpoints import (
    partners, users, licenses, attractions,
    attraction_aggregates, partner_aggregates
)

api_router = APIRouter()
api_router.include_router(
    attraction_aggregates.router,
    prefix=URLPathsConfig.PREFIX + "/attraction_aggregates",
    tags=["Attraction Aggregates"]
)
api_router.include_router(
    partner_aggregates.router,
    prefix=URLPathsConfig.PREFIX + "/partner_aggregates",
    tags=["Partner Aggregates"]
)
api_router.include_router(
    attractions.router,
    prefix=URLPathsConfig.PREFIX + "/attractions",
    tags=["Attractions"]
)
api_router.include_router(
    users.router,
    prefix=URLPathsConfig.PREFIX + "/users",
    tags=["Users"]
)
api_router.include_router(
    partners.router,
    prefix=URLPathsConfig.PREFIX + "/partners",
    tags=["Partners"]
)
api_router.include_router(
    licenses.router,
    prefix=URLPathsConfig.PREFIX + "/licenses",
    tags=["Licenses"]
)
