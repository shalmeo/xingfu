from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.uncertain.interfaces.uow import IUncertainUoW
from src.application.uncertain.usecases.uncertain import GetUncertain
from src.bot.constants import MISS
from src.bot.keyboards.root.uncertains.callback_data import (
    UncertainCallbackData,
    UncertainAction,
)
from src.bot.keyboards.root.uncertains.info import get_uncertain_info_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(UncertainCallbackData.filter(F.action == UncertainAction.INFO))
async def on_uncertain_info(
    c: types.CallbackQuery,
    callback_data: UncertainCallbackData,
    uow: IUncertainUoW,
    ftl: TranslatorRunner,
):
    uncertain = await GetUncertain(uow)(callback_data.uncertain_id)
    text = ftl.root.profile.registry.uncertain.info(
        surname=uncertain.surname,
        name=uncertain.name,
        patronymic=uncertain.patronymic or MISS,
        phone=f"+{uncertain.user.phone}" if uncertain.user.phone else MISS,
        email=uncertain.user.email,
        telegram_id=str(uncertain.user.telegram_id)
        if uncertain.user.telegram_id
        else MISS,
        username=uncertain.user.telegram_username or MISS,
        birthday=uncertain.birthday,
        timezone=uncertain.user.timezone,
    )
    markup = get_uncertain_info_markup(ftl, callback_data.uncertain_id)
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()
