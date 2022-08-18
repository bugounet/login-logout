from fastapi import APIRouter

from msio.logme.api.v1.login_logout import router as login_router
from msio.logme.api.v1.users import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(users_router)
