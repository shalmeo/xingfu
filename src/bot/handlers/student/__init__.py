from aiogram import Router
from src.bot.filters.student.access import StudentAccessFilter

from src.bot.handlers.student import start


def setup() -> Router:
    router = Router()

    router.message.filter(StudentAccessFilter())
    router.callback_query.filter(StudentAccessFilter())

    router.include_router(start.router)

    return router
