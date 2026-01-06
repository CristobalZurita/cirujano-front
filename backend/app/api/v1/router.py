from fastapi import APIRouter
from .endpoints import brands, instruments, auth

# Routers adicionales (creados por copilot) - si existen, se incluyen
try:
	from backend.app.routers import user as user_router
	from backend.app.routers import repair as repair_router
	from backend.app.routers import instrument as instrument_router
	from backend.app.routers import category as category_router
	from backend.app.routers import stock_movement as stock_movement_router
	from backend.app.routers import contact as contact_router
except Exception:
	# Si los módulos no existen en este entorno, se ignoran
	user_router = repair_router = instrument_router = category_router = stock_movement_router = contact_router = None

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(brands.router)
api_router.include_router(instruments.router)
api_router.include_router(auth.router)

# Incluir routers adicionales si están disponibles
if user_router:
	api_router.include_router(user_router.router)
if repair_router:
	api_router.include_router(repair_router.router)
if instrument_router:
	api_router.include_router(instrument_router.router)
if category_router:
	api_router.include_router(category_router.router)
if stock_movement_router:
	api_router.include_router(stock_movement_router.router)
if contact_router:
	api_router.include_router(contact_router.router)
