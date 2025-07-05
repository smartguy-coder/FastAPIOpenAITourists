from apps.tourism.router import router_tourism
from fastapi import FastAPI
from settings import settings


def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        root_path="/api",
    )

    app.include_router(router_tourism, prefix="/tourism", tags=["Tourism"])

    return app
