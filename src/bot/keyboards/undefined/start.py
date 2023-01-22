from typing import TYPE_CHECKING

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_start_markup(
    ftl: TranslatorRunner, base_url: str, telegram_id: int, telegram_username: str
) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=ftl.undefined.start.review.button()),
            KeyboardButton(text=ftl.undefined.start.games.button()),
        ],
        [
            KeyboardButton(text=ftl.undefined.start.open.day.button()),
            KeyboardButton(text=ftl.undefined.start.invite.parent.button()),
        ],
        [
            KeyboardButton(
                text=ftl.undefined.start.request.trial.lesson.button(),
                web_app=WebAppInfo(
                    url=ftl.web.undefined.sign.up.url(
                        base_url=base_url, telegram_id=str(telegram_id), telegram_username=telegram_username
                    )
                ),
            ),
            KeyboardButton(text=ftl.undefined.start.invite.student.button()),
        ],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
