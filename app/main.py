import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.routers import users, spots, login

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Lifespan context manager to create DB tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting up {settings.APP_NAME}...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(users.router, tags=["Users"])
app.include_router(spots.router, tags=["Spots"])
app.include_router(login.router, tags=["Login"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the main map page.
    """
    logger.info("Serving root page (map).")
    return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.APP_NAME})