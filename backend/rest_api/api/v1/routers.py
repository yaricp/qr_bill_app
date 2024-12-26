from fastapi import APIRouter

from ..config import URLPathsConfig
from .endpoints import (
    goods, sellers, users, categories, bills, units
)

api_router = APIRouter()
api_router.include_router(
    bills.router,
    prefix=URLPathsConfig.PREFIX + "/bills",
    tags=["Bills"]
)
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
    goods.router,
    prefix=URLPathsConfig.PREFIX + "/goods",
    tags=["Goods"]
)
api_router.include_router(
    units.router,
    prefix=URLPathsConfig.PREFIX + "/units",
    tags=["Units"]
)
api_router.include_router(
    categories.router,
    prefix=URLPathsConfig.PREFIX + "/categories",
    tags=["Categories"]
)
