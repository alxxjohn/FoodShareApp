from fastapi.routing import APIRouter

from foodshareapp.app.api.routes import docs, echo, foodInsecurePerson, health, register


api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(docs.router)
api_router.include_router(foodInsecurePerson.router, prefix="/user", tags=["Food Insecure Person"])
api_router.include_router(register.router, prefix="/register", tags=["Register"])
api_router.include_router(echo.router, prefix="/echo", tags=["Echo"])
