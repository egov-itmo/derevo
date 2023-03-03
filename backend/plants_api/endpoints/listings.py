"""
listing endpoints are defined here.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.logic.listings import (
    get_humidity_types_from_db,
    get_light_types_from_db,
    get_limitation_factors_from_db,
    get_soil_acidity_types_from_db,
    get_soil_fertility_types_from_db,
    get_soil_types_from_db,
)
from plants_api.schemas import ListingResponse

api_router = APIRouter(tags=["listing"])


@api_router.get(
    "/listing/humidity_types",
    response_model=ListingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_humidity_types(connection: AsyncConnection = Depends(get_connection)) -> ListingResponse:
    """
    Get list of humidity types consisting of identificators and names.
    """
    acidity_types = await get_humidity_types_from_db(connection)
    return ListingResponse.from_dtos(acidity_types)


@api_router.get(
    "/listing/light_types",
    response_model=ListingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_light_types(connection: AsyncConnection = Depends(get_connection)) -> ListingResponse:
    """
    Get list of light types consisting of identificators and names.
    """
    acidity_types = await get_light_types_from_db(connection)
    return ListingResponse.from_dtos(acidity_types)


@api_router.get(
    "/listing/limitation_factors",
    response_model=ListingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_limitation_factors(connection: AsyncConnection = Depends(get_connection)) -> ListingResponse:
    """
    Get list of limitation factors consisting of identificators and names.
    """
    acidity_types = await get_limitation_factors_from_db(connection)
    return ListingResponse.from_dtos(acidity_types)


@api_router.get(
    "/listing/soil_acidity_types",
    response_model=ListingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_soil_acidity_types(connection: AsyncConnection = Depends(get_connection)) -> ListingResponse:
    """
    Get list of soil acidity types consisting of identificators and names.
    """
    acidity_types = await get_soil_acidity_types_from_db(connection)
    return ListingResponse.from_dtos(acidity_types)


@api_router.get(
    "/listing/soil_fertility_types",
    response_model=ListingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_soil_fertility_types(connection: AsyncConnection = Depends(get_connection)) -> ListingResponse:
    """
    Get list of soil fertility types consisting of identificators and names.
    """
    acidity_types = await get_soil_fertility_types_from_db(connection)
    return ListingResponse.from_dtos(acidity_types)


@api_router.get(
    "/listing/soil_types",
    response_model=ListingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_soil_types(connection: AsyncConnection = Depends(get_connection)) -> ListingResponse:
    """
    Get list of soil types consisting of identificators and names.
    """
    acidity_types = await get_soil_types_from_db(connection)
    return ListingResponse.from_dtos(acidity_types)
