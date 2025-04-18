from typing import Awaitable, Callable
from httpx import AsyncClient as http_client
from fastapi import FastAPI

# from foodshareapp.settings import settings


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    inthe state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        from foodshareapp.db.utils import db

        await db.connect()
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        from foodshareapp.db.utils import db, redis_db

        await db.disconnect()
        await redis_db.connection_pool.disconnect()
        await http_client.aclose()
        pass  # noqa: WPS420

    return _shutdown
