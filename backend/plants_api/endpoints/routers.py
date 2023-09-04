"""
Api routers are defined here.

It is needed to import files which use this routers to initialize endpoints.
"""
from fastapi import APIRouter

from .update import update_router
from .users import user_data_router


limitations_router = APIRouter(tags=["limitations"], prefix="/limitations")

system_router = APIRouter(tags=["system"])

listing_router = APIRouter(tags=["listing"], prefix="/listing")

plants_router = APIRouter(tags=["plants"], prefix="/plants")

compositions_router = APIRouter(tags=["compositions"], prefix="/compositions")

routers_list = [
    system_router,
    listing_router,
    plants_router,
    compositions_router,
    limitations_router,
    update_router,
    user_data_router,
]

__all__ = [
    "routers_list",
]
