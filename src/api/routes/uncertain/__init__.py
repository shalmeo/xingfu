from fastapi import APIRouter

from src.api.routes.uncertain import sign_up

router = APIRouter(tags=["Uncertain"])


router.include_router(sign_up.router)
