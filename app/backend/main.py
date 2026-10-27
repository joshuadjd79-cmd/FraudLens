"""
FraudLens — Full-Stack Financial Fraud Detection & Investigation Platform
FastAPI Application Entrypoint

Features:
- Pure Python Oracle 26ai Free connectivity via oracledb thin mode
- Automatic in-memory fallback adapter with visible mode flags if Oracle is offline
- REST endpoints for Transactions, Alerts, Investigations, Audit, and Analytics
- Lifespan database connection pooling
- CORS configuration for local Vite frontend
- Comprehensive OpenAPI interactive documentation at /docs
"""

from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.backend.config import settings
from app.backend.database.connection import init_db_pool, close_db_pool, check_oracle_health
from app.backend.routers import (
    health,
    dashboard,
    transactions,
    alerts,
    investigations,
    audit,
    analytics,
    demo,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("fraudlens")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes Oracle connection pool on startup and gracefully releases on shutdown.
    """
    logger.info("Initializing FraudLens backend service...")
    try:
        init_db_pool()
        logger.info("Database pool initialization sequence completed.")
    except Exception as e:
        logger.warning(f"Database pool setup encountered non-fatal error: {e}. Demo mode active.")

    yield

    logger.info("Shutting down FraudLens backend service...")
    try:
        close_db_pool()
        logger.info("Database pool closed successfully.")
    except Exception as e:
        logger.error(f"Error during pool closure: {e}")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "FraudLens Financial Fraud Detection & Investigation Platform REST API. "
        "Built on Oracle Database 26ai Free with PL/SQL stored procedures, triggers, "
        "and real-time rule-based risk evaluation."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global safe exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    # Sanitize message to never leak raw passwords
    safe_msg = str(exc)
    if settings.oracle_password and settings.oracle_password in safe_msg:
        safe_msg = safe_msg.replace(settings.oracle_password, "********")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An internal server error occurred while processing the request.",
            "data": None,
            "error_detail": safe_msg,
        },
    )


# Include API Routers with /api prefix
app.include_router(health.router)
app.include_router(dashboard.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(investigations.router, prefix="/api")
app.include_router(investigations.investigators_router, prefix="/api")
app.include_router(audit.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(demo.router, prefix="/api")


@app.get("/", tags=["System"])
def root():
    """Root landing endpoint with system status and documentation links."""
    oracle_health = check_oracle_health()
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "ONLINE",
        "database_mode": "ORACLE_LIVE" if oracle_health["healthy"] else "DEMO_FALLBACK",
        "docs_url": "/docs",
        "api_prefix": "/api",
        "oracle_connected": oracle_health["healthy"],
    }
