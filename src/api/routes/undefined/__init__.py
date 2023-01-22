from fastapi import APIRouter

from src.api.routes.undefined import sign_up

router = APIRouter(tags=["Undefined"])


router.include_router(sign_up.router)
