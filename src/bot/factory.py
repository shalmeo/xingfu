import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from sqlalchemy.orm import sessionmaker

from src.infrastructure.localization.fluent import FluentAdapter
from src.bot import handlers, middlewares

logger = logging.getLogger(__name__)


def create_bot(token: str):
    return Bot(token=token, parse_mode="HTML")


def create_dispatcher(
    storage: BaseStorage,
    fluent: FluentAdapter,
    session_factory: sessionmaker,
    base_url: str,
    bot_admins: list[int],
):
    dispatcher = Dispatcher(storage=storage)
    dispatcher["base_url"] = base_url
    dispatcher["bot_admins"] = bot_admins
    handlers.setup(dispatcher)
    middlewares.setup(dispatcher, fluent, session_factory)

    return dispatcher
