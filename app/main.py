from fastapi import FastAPI

from app.api.routes.costs import router as costs_router
from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.posts import router as posts_router
from app.api.routes.suggestions import router as suggestions_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.app_name, debug=settings.app_debug)

app.include_router(health_router)
app.include_router(posts_router)
app.include_router(suggestions_router)
app.include_router(jobs_router)
app.include_router(costs_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Image Matching Engine API"}
