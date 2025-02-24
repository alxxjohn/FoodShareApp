from fastapi import APIRouter
from foodshareapp.db.utils import redis_db

router = APIRouter()


@router.get("/health")
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """


@router.get("/data")
def rediget(value: str) -> str:
    redis_db.set(value)
    return value
