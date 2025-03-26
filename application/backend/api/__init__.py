from fastapi import APIRouter

from .employees.views import router as employees_router

router = APIRouter()
router.include_router(router=employees_router, prefix="/employees")