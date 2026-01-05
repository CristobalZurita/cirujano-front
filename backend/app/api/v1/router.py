from fastapi import APIRouter
from .endpoints import brands, instruments

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(brands.router)
api_router.include_router(instruments.router)
