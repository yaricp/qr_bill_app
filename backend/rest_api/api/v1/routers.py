from fastapi import APIRouter

from ..config import URLPathsConfig
from .endpoints import (
    sellers, users, purchases, categories
)

api_router = APIRouter()
api_router.include_router(
    sellers.router,
    prefix=URLPathsConfig.PREFIX + "/sellers",
    tags=["Sellers"]
)
api_router.include_router(
    users.router,
    prefix=URLPathsConfig.PREFIX + "/users",
    tags=["Users"]
)
api_router.include_router(
    purchases.router,
    prefix=URLPathsConfig.PREFIX + "/purchases",
    tags=["Purchases"]
)
api_router.include_router(
    categories.router,
    prefix=URLPathsConfig.PREFIX + "/categories",
    tags=["Categories"]
)
