from fastapi import APIRouter

from . import create
from . import get
from . import update

router = APIRouter()

router.include_router(create.router)
router.include_router(get.router)
router.include_router(update.router)
