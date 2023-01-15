from aiogram import Router

from . import registry
from . import info


def setup():
    router = Router()

    router.include_router(registry.router)
    router.include_router(info.router)

    return router
