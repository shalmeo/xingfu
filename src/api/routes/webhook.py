from aiogram import Dispatcher, Bot
from aiogram.types import Update
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import SecretStr
from starlette import status

from src.api.providers import secret_provider, bot_provider, dispatcher_provider

router = APIRouter(prefix="/telegram-webhook", tags=["Telegram Webhook"])


@router.post("")
async def webhook_route(
    update: Update,
    secret: SecretStr = Header(alias="X-Telegram-Bot-Api-Secret-Token"),
    expected_secret: str = Depends(secret_provider),
    bot: Bot = Depends(bot_provider),
    dispatcher: Dispatcher = Depends(dispatcher_provider),
):
    if secret.get_secret_value() != expected_secret:
        raise HTTPException(
            detail="Invalid secret", status_code=status.HTTP_401_UNAUTHORIZED
        )

    await dispatcher.feed_update(bot, update=update)
    return {"ok": True}
