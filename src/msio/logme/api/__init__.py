from fastapi import APIRouter

from msio.logme.api.health import router as health_router
from msio.logme.api.v1 import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(health_router)
router.include_router(v1_router)
