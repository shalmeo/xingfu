from aiogram import Router

from src.bot.filters.root.access import RootAccessFilter
from src.bot.handlers.root import (
    start,
    profile,
    admins,
    teachers,
    students,
    groups,
    uncertains,
)


def setup() -> Router:
    router = Router()

    router.message.filter(RootAccessFilter())
    router.callback_query.filter(RootAccessFilter())

    router.include_router(admins.setup())
    router.include_router(teachers.setup())
    router.include_router(students.setup())
    router.include_router(groups.setup())
    router.include_router(uncertains.setup())
    router.include_router(profile.router)
    router.include_router(start.router)

    return router
