import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from src.api.factory import create_application
from src.api.providers import (
    bot_provider,
    webhook_url_provider,
    secret_provider,
    dispatcher_provider,
)
from src.bot.factory import create_bot, create_dispatcher
from src.configure import configure_logging, configure_fluent, configure_postgres
from src.settings import get_settings

logger = logging.getLogger(__name__)


def get_application():
    configure_logging()
    logger.info("Starting bot")

    settings = get_settings()
    session_factory = configure_postgres(settings.postgres.url)
    fluent = configure_fluent()
    storage = RedisStorage.from_url(url=settings.redis.url)
    bot = create_bot(token=settings.bot_token)
    dispatcher = create_dispatcher(
        storage=storage,
        fluent=fluent,
        session_factory=session_factory,
        base_url=settings.web.base_url,
        bot_admins=settings.bot_admins,
    )
    return create_application(
        bot=bot,
        dispatcher=dispatcher,
        webhook_secret=settings.webhook.secret,
        postgres_url=settings.postgres.url,
        webhook_url=settings.webhook.url,
        bot_admins=settings.bot_admins,
    )


app = get_application()


@app.on_event("startup")
async def startup_event():
    bot: Bot = app.dependency_overrides.get(bot_provider)()
    webhook_url: str = app.dependency_overrides.get(webhook_url_provider)()
    secret: str = app.dependency_overrides.get(secret_provider)()

    await bot.delete_webhook()
    await bot.set_webhook(
        url=webhook_url, drop_pending_updates=True, secret_token=secret
    )


@app.on_event("shutdown")
async def shutdown_event():
    bot: Bot = app.dependency_overrides.get(bot_provider)()
    dispatcher: Dispatcher = app.dependency_overrides.get(dispatcher_provider)()

    await bot.session.close()
    await dispatcher.storage.close()
