"""
Cirujano de Sintetizadores - Backend API
Sistema integral de gestión para taller de reparación de sintetizadores

FastAPI application with async database support, JWT authentication,
and comprehensive diagnostic/quotation system.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan context manager for app startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here
    logger.info("Application startup")
    yield
    # Shutdown logic here
    logger.info("Application shutdown")


# Initialize FastAPI app
app = FastAPI(
    title="Cirujano de Sintetizadores API",
    description="Sistema integral de gestión para taller de reparación de sintetizadores",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with actual frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


# Error handling
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
