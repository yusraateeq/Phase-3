"""
Todo Backend API - FastAPI application entry point.
Initializes the FastAPI app with middleware, CORS, and route handlers.

IMPORTANT: This file should be run via run_backend.py or with PYTHONPATH set.
If importing fails with "No module named 'core'", see backend/START_HERE.md
"""
# CRITICAL: Must be first import - sets up path before anything else
import sys
import os
from pathlib import Path

_backend_dir = Path(__file__).parent.resolve()
_src_dir = _backend_dir / "src"
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))
# Ensure PYTHONPATH is set for subprocess calls (e.g., from SmartAgent)
os.environ["PYTHONPATH"] = f"{_src_dir}{os.pathsep}{os.environ.get('PYTHONPATH', '')}"
os.chdir(str(_backend_dir))

# Now safe to import from src modules
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import create_db_and_tables
from middleware.logging import LoggingMiddleware
from middleware.errors import ErrorHandlingMiddleware
from api import auth as auth_router
from api import tasks as tasks_router
from api import chat as chat_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup: Create database tables
    logger.info("Starting application...")
    logger.info("Creating database tables...")
    create_db_and_tables()
    logger.info("Database tables created successfully")

    yield

    # Shutdown
    logger.info("Shutting down application...")


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern, secure, multi-user todo application with JWT authentication",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Add custom middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)


# Add CORS middleware (must be last to be the outermost layer)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG
    }


# API Routes
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks_router.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
