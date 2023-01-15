from fastapi import Request
from starlette.responses import JSONResponse

from src.application.common.exceptions.common import AlreadyExists


async def conflict_error(request: Request, exc: AlreadyExists):
    return JSONResponse(status_code=409, content={"detail": str(exc)})
