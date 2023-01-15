from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from src.infrastructure.localization.fluent import FluentAdapter
from src.bot.middlewares.database import DatabaseMiddleware
from src.bot.middlewares.lang import LangMiddleware


def setup(dp: Dispatcher, fluent: FluentAdapter, session_maker: sessionmaker):
    dp.message.outer_middleware.register(LangMiddleware(fluent))
    dp.callback_query.outer_middleware.register(LangMiddleware(fluent))

    dp.message.outer_middleware.register(DatabaseMiddleware(session_maker))
    dp.callback_query.outer_middleware.register(DatabaseMiddleware(session_maker))
