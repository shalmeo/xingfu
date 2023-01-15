from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import providers
from src.api.error_handlers.conflict import conflict_error
from src.api.error_handlers.not_found import not_found_error
from src.api.routes import webhook, root
from src.api.spa import SinglePageApplication
from src.application.common.exceptions.common import NotFound, AlreadyExists


def create_application(
    bot: Bot,
    dispatcher: Dispatcher,
    webhook_secret: str,
    postgres_url: str,
    webhook_url: str,
    bot_admins: list[int],
) -> FastAPI:
    application = FastAPI()

    application.include_router(root.router)
    application.include_router(webhook.router)
    application.mount(
        "/",
        app=SinglePageApplication("/home/shalmeo/projects/xingfu/frontend/dist"),
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
        providers.session_provider: providers.session(postgres_url),
        providers.uow_provider: providers.uow,
        providers.bot_provider: lambda: bot,
        providers.dispatcher_provider: lambda: dispatcher,
        providers.secret_provider: lambda: webhook_secret,
        providers.webhook_url_provider: lambda: webhook_url,
        providers.bot_admins_provider: lambda: bot_admins,
    }

    return application
