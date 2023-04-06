"""
Redirection from / and /api to swagger-ui is defined here.
"""
import fastapi
from starlette import status

from .routers import system_router


@system_router.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
@system_router.get("/api/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_swagger_docs():
    "Redirects to **/docs** from **/**"
    return fastapi.responses.RedirectResponse("/api/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
