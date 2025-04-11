from fastapi import APIRouter

from .index import router as index_router
from .employees import router as employees_router
from .objects import router as object_router
from .sanitary_breaks import router as sanitary_breaks_router

router = APIRouter()
router.include_router(router=index_router)
router.include_router(router=employees_router, prefix="/employees")
router.include_router(router=object_router, prefix="/objects")
router.include_router(router=sanitary_breaks_router, prefix="/sanitary_breaks")
