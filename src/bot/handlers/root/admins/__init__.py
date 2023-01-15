from aiogram import Router

from . import registry
from . import info

from . import export

# from . import impor
from . import delete


def setup():
    router = Router()

    router.include_router(registry.router)
    router.include_router(info.router)
    router.include_router(export.router)
    # router.include_router(impor.router)
    router.include_router(delete.router)

    return router
