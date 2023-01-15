from aiogram import Router

from src.bot.handlers.uncertain import start


def setup() -> Router:
    router = Router()

    router.include_router(start.router)

    return router
