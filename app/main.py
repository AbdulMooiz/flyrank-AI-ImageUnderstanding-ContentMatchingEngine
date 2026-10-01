from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.app_name, debug=settings.app_debug)

app.include_router(health_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Image Matching Engine API"}
