from fastapi import Request
from starlette.responses import JSONResponse

from src.application.common.exceptions.common import NotFound


async def not_found_error(request: Request, exc: NotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
