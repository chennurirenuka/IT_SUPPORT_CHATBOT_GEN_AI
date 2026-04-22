from fastapi import FastAPI
from app.routes import router
from app.core.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.include_router(router)

@app.on_event("startup")
def startup_event():
    logger.info("Application started")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Application stopped")
