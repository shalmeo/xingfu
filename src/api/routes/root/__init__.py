from fastapi import APIRouter

from src.api.routes.root import admin
from src.api.routes.root import teacher
from src.api.routes.root import student

from src.api.routes.root import group

router = APIRouter(prefix="/root", tags=["Root"])

router.include_router(admin.router)
router.include_router(teacher.router)
router.include_router(student.router)
router.include_router(group.router)
