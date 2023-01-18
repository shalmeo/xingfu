from aiogram import Bot, Dispatcher
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import providers
from src.api.error_handlers.conflict import conflict_error
from src.api.error_handlers.not_found import not_found_error
from src.api.routes import webhook, root, uncertain
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

    api_router = APIRouter(prefix="/api")
    api_router.include_router(root.router)
    api_router.include_router(uncertain.router)
    
    application.include_router(webhook.router)

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
        providers.sm_provider: lambda: providers.sm(postgres_url),
        providers.uow_provider: providers.uow,
        providers.bot_provider: lambda: bot,
        providers.dispatcher_provider: lambda: dispatcher,
        providers.secret_provider: lambda: webhook_secret,
        providers.webhook_url_provider: lambda: webhook_url,
        providers.bot_admins_provider: lambda: bot_admins,
    }

    return application
