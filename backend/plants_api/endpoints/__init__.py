"""
All FastApi endpoints are exported from this module.
"""
from plants_api.endpoints.health_check import api_router as health_check
from plants_api.endpoints.listings import api_router as listings
from plants_api.endpoints.plants import api_router as plants
from plants_api.endpoints.redirect_to_swagger import api_router as redirect_to_swagger
from plants_api.endpoints.update import api_router as update

list_of_routes = [
    health_check,
    listings,
    plants,
    redirect_to_swagger,
    update,
]


__all__ = [
    "list_of_routes",
]
