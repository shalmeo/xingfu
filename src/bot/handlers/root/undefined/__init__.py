from aiogram import Router

from . import registry
from . import info

from . import accept
from . import reject


def setup():
    router = Router()

    router.include_router(registry.router)
    router.include_router(info.router)
    router.include_router(accept.router)
    router.include_router(reject.router)

    return router
