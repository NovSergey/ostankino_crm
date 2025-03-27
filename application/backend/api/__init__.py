from fastapi import APIRouter

from .employees.views import router as employees_router
from .positions.views import router as positions_router

router = APIRouter()
router.include_router(router=employees_router, prefix="/employees")
router.include_router(router=positions_router, prefix="/positions")