from aiogram import Router

from . import registry
from . import info
from . import delete
from . import export

# from . import impor


def setup():
    router = Router()

    router.include_router(registry.router)
    router.include_router(info.router)
    router.include_router(delete.router)
    router.include_router(export.router)
    # router.include_router(impor.router)

    return router
