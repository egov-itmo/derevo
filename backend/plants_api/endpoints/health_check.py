"""
health_check endpoint is defined here.
"""
from fastapi import APIRouter
from starlette import status

from plants_api.schemas import PingResponse

api_router = APIRouter(tags=["Health check"])


@api_router.get(
    "/health_check/ping",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
)
async def health_check():
    """
    Return health check response.
    """
    return PingResponse()
