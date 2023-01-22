import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.orm import sessionmaker

from src.api.factory import create_application
from src.bot.factory import create_bot, create_dispatcher
from src.configure import configure_logging, configure_fluent, configure_postgres
from src.infrastructure.database.init import add_initial_admins
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
        session_factory=session_factory,
        webhook_url=settings.webhook.url,
        bot_admins=settings.bot_admins,
        use_spa=settings.web.use_spa,
    )


app = get_application()


@app.on_event("startup")
async def startup_event():
    bot: Bot = app.state.bot
    webhook_url: str = app.state.webhook_url
    secret: str = app.state.secret
    bot_admins = app.state.bot_admins
    sm: sessionmaker = app.state.sessionmaker

    await bot.delete_webhook()
    await bot.set_webhook(url=webhook_url, drop_pending_updates=True, secret_token=secret)
    await add_initial_admins(sm, bot_admins)


@app.on_event("shutdown")
async def shutdown_event():
    bot: Bot = app.state.bot
    dispatcher: Dispatcher = app.state.dispatcher

    await bot.session.close()
    await dispatcher.storage.close()
