from importlib import metadata
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics


from foodshareapp_api.app.api.router import api_router
from foodshareapp_api.app.lifetime import (register_shutdown_event,
                                           register_startup_event)

APP_ROOT = Path(__file__).parent.parent


tags_metadata = [
    {
        "name": "register",
        "description": "Operations for registering a user.",
    }
]


class APIKeyFilterMiddleware(BaseHTTPMiddleware):
    """HTTP middleware that returns 401 if the header does not match
    the one in config.
    Routes in `UNFILTERED_ROUTES` are always allowed through.
    Requests with `referer` header equal to any value in `UNFILTERED_REQUESTS`
    are always allowed through.
    """

    UNFILTERED_ROUTES = {
        "/docs",
        "/favicon.ico",
        "/redoc",
        "/openapi.json",
        "/webhooks/stripe/payment-intent",
        "/webhooks/stripe/checkout-session",
        "/health_check"
    }


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=[
                "*"
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    app = FastAPI(
        middleware=middleware,
        title="Foodshare App API",
        description="Foodshare backend api end points",
        version=metadata.version("foodshareapp_api"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        openapi_tags=tags_metadata,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix='/api')
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    return app


app = get_app()


app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.middleware("http")
async def add_version_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Version"] = app.version
    return response
