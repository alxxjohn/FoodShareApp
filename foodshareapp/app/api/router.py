from fastapi.routing import APIRouter

from foodshareapp.app.api.routes import docs, echo, health, register


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(register.router, prefix="/register", tags=["register"])
