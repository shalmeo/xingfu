from aiogram import Bot, Dispatcher
from fastapi import APIRouter, FastAPI
from sqlalchemy.orm import sessionmaker
from starlette.middleware.cors import CORSMiddleware

from src.api import providers
from src.api.error_handlers.conflict import conflict_error
from src.api.error_handlers.not_found import not_found_error
from src.api.routes import webhook, root, undefined
from src.api.spa import SinglePageApplication
from src.application.common.exceptions.common import NotFound, AlreadyExists


def create_application(
    bot: Bot,
    dispatcher: Dispatcher,
    webhook_secret: str,
    session_factory: sessionmaker,
    webhook_url: str,
    bot_admins: list[int],
    use_spa: bool,
) -> FastAPI:
    application = FastAPI()

    application.state.bot = bot
    application.state.dispatcher = dispatcher
    application.state.webhook_url = webhook_url
    application.state.secret = webhook_secret
    application.state.bot_admins = bot_admins
    application.state.sessionmaker = session_factory

    api_router = APIRouter(prefix="/api")
    api_router.include_router(root.router)
    api_router.include_router(undefined.router)

    application.include_router(api_router)
    application.include_router(webhook.router)

    if use_spa:
        application.mount(
            "/",
            app=SinglePageApplication("/home/shalmeo/projects/xingfu/backend/dist"),
            name="SPA",
        )

    application.add_exception_handler(NotFound, not_found_error)
    application.add_exception_handler(AlreadyExists, conflict_error)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.dependency_overrides = {
        providers.session_provider: providers.session(session_factory),
        providers.uow_provider: providers.uow,
        providers.bot_provider: lambda: bot,
        providers.dispatcher_provider: lambda: dispatcher,
        providers.secret_provider: lambda: webhook_secret,
    }

    return application
