from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update

from src.infrastructure.localization.fluent import FluentAdapter


class LangMiddleware(BaseMiddleware):
    def __init__(self, fluent: FluentAdapter):
        self.fluent = fluent

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        ftl = self.fluent.get_translator_by_locale()
        data["ftl"] = ftl
        await handler(event, data)
        data.pop("ftl")
