"""
Cirujano de Sintetizadores - Backend API
Sistema integral de gestión para taller de reparación de sintetizadores

FastAPI application with async database support, JWT authentication,
and comprehensive diagnostic/quotation system.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from backend.app.core.config import settings
from backend.app.core.database import init_db, close_db
from backend.app.api.v1.router import api_router
from backend.app.core.ratelimit import limiter
from slowapi.errors import RateLimitExceeded


async def _rate_limit_exceeded_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan context manager for app startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("🚀 Application startup")
    try:
        await init_db()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
    
    yield
    
    # Shutdown logic
    logger.info("🛑 Application shutdown")
    try:
        await close_db()
        logger.info("✓ Database connection closed")
    except Exception as e:
        logger.error(f"✗ Error during shutdown: {e}")


# Initialize FastAPI app
app = FastAPI(
    title="Cirujano de Sintetizadores API",
    description="Sistema integral de gestión para taller de reparación de sintetizadores",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Configure CORS with settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS configured for origins: {settings.allowed_origins}")

# Enforce HTTPS and add basic security headers when running in production
if settings.environment and settings.environment.lower() in ("production", "prod"):
    # Redirect HTTP to HTTPS
    app.add_middleware(HTTPSRedirectMiddleware)

    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        # HSTS: 2 years, include subdomains, preload
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response


    # Attach rate limiter to the application state and register handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API v1 routes
app.include_router(api_router)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Cirujano de Sintetizadores API is running"}


# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "Cirujano de Sintetizadores",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


# Error handling
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=settings.DEBUG)
