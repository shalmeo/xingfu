from typing import TYPE_CHECKING

from aiogram import Router, F, types
from fluentogram import TranslatorRunner

from src.application.uncertain.interfaces.uow import IUncertainUoW
from src.application.uncertain.usecases.uncertain import DeleteUncertain
from src.bot.keyboards.root.uncertains.callback_data import (
    UncertainCallbackData,
    UncertainAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(UncertainCallbackData.filter(F.action == UncertainAction.REJECT))
async def on_reject_uncertain(
    c: types.CallbackQuery,
    callback_data: UncertainCallbackData,
    uow: IUncertainUoW,
    ftl: TranslatorRunner,
):
    await DeleteUncertain(uow)(callback_data.uncertain_id)
    text = ftl.root.profile.registry.uncertain.successfully.rejected()
    await c.message.delete()
    await c.message.answer(text)
