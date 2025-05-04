from fastapi import APIRouter, Depends

from .index import router as index_router
from .employees import router as employees_router
from .objects import router as object_router
from .sanitary_breaks import router as sanitary_breaks_router
from .settings import router as settings_router
from .visit_history import router as visit_history_router
from .notifications import router as notifications_router

router = APIRouter()
router.include_router(router=index_router)
router.include_router(router=employees_router, prefix="/employees")
router.include_router(router=object_router, prefix="/objects")
router.include_router(router=visit_history_router, prefix="/visit_history")
router.include_router(router=sanitary_breaks_router, prefix="/sanitary_breaks")
router.include_router(router=settings_router, prefix="/settings")
router.include_router(router=notifications_router, prefix="/notifications")
