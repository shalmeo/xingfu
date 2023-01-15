from aiogram import Bot, Dispatcher


def bot_provider() -> Bot:
    ...


def dispatcher_provider() -> Dispatcher:
    ...


def secret_provider() -> str:
    ...


def webhook_url_provider() -> str:
    ...


def bot_admins_provider() -> list[int]:
    ...
