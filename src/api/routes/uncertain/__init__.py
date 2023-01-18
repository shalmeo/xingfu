from fastapi import APIRouter

from src.api.routes.uncertain import sign_up

router = APIRouter(prefix="/uncertain", tags=["Uncertain"])


router.include_router(sign_up.router)
