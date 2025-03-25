from fastapi.routing import APIRouter

from foodshareapp.app.api.routes import (
    docs,
    echo,
    foodInsecurePerson,
    health,
    register,
    reservations,
    inventory,
    foodbanks,
    auth,
)


api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(docs.router)
api_router.include_router(
    foodInsecurePerson.router, prefix="/person", tags=["Food Insecure Person"]
)
api_router.include_router(register.router, prefix="/register", tags=["Register"])
api_router.include_router(echo.router, prefix="/echo", tags=["Echo"])
api_router.include_router(
    reservations.router, prefix="/reservations", tags=["Reservations"]
)
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(foodbanks.router, prefix="/foodbanks", tags=["Food Banks"])
api_router.include_router(auth.router, prefix="/login", tags=["Auth"])
