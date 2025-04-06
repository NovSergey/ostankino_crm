from fastapi import APIRouter

from .employees.views import router as employees_router
from .groups.views import router as groups_router

router = APIRouter()
router.include_router(router=employees_router, prefix="/employees")
router.include_router(router=groups_router, prefix="/groups")