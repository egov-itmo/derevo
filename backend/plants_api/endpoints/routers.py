"""
Api routers are defined here.

It is needed to import files which use this routers to initialize endpoints.
"""
from fastapi import APIRouter

limitations_router = APIRouter(tags=["Limitations"], prefix="/get_limitations")

health_check_router = APIRouter(tags=["Health check"])

listing_router = APIRouter(tags=["listing"], prefix="/listing")

plants_router = APIRouter(tags=["plants"], prefix="/plants")

update_router = APIRouter(tags=["update"], prefix="/update")

routers_list = [
    limitations_router,
    health_check_router,
    listing_router,
    plants_router,
    update_router,
]

__all__ = [
    "routers_list",
]
