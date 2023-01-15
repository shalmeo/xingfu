from aiogram import Dispatcher, F

from src.bot.handlers import root
from src.bot.handlers import uncertain
from src.bot.handlers import error


def setup(dispatcher: Dispatcher):
    dispatcher.message.filter(F.chat.type == "private")
    dispatcher.callback_query.filter(F.message.chat.type == "private")

    # dispatcher.include_router(error.router)
    dispatcher.include_router(root.setup())
    dispatcher.include_router(uncertain.setup())
