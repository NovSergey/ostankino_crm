from fastapi import APIRouter

from .employees.views import router as employees_router
from .groups.views import router as groups_router
from .visit_history.views import router as visit_history_router
from .objects.views import router as objects_router

router = APIRouter()
router.include_router(router=employees_router, prefix="/employees")
router.include_router(router=groups_router, prefix="/groups")
router.include_router(router=objects_router, prefix="/objects")
router.include_router(router=visit_history_router, prefix="/visit_history")
