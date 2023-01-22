from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.undefined.interfaces.uow import IUndefinedUoW
from src.application.undefined.usecases.undefined import GetUndefined
from src.bot.constants import MISS
from src.bot.keyboards.root.undefined.callback_data import (
    UndefinedCallbackData,
    UndefinedAction,
)
from src.bot.keyboards.root.undefined.info import get_undefined_info_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(UndefinedCallbackData.filter(F.action == UndefinedAction.INFO))
async def on_undefined_info(
    c: types.CallbackQuery,
    callback_data: UndefinedCallbackData,
    uow: IUndefinedUoW,
    ftl: TranslatorRunner,
):
    undefined = await GetUndefined(uow)(callback_data.undefined_id)
    text = ftl.root.profile.registry.undefined.info(
        surname=undefined.surname,
        name=undefined.name,
        patronymic=undefined.patronymic or MISS,
        phone=f"+{undefined.user.phone}" if undefined.user.phone else MISS,
        email=undefined.user.email,
        telegram_id=str(undefined.user.telegram_id) if undefined.user.telegram_id else MISS,
        username=undefined.user.telegram_username or MISS,
        birthday=undefined.birthday,
        timezone=undefined.user.timezone,
    )
    markup = get_undefined_info_markup(ftl, callback_data.undefined_id)
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()
