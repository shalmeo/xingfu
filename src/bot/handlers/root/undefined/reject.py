from typing import TYPE_CHECKING

from aiogram import Router, F, types
from fluentogram import TranslatorRunner

from src.application.undefined.interfaces.uow import IUndefinedUoW
from src.application.undefined.usecases.undefined import DeleteUndefined
from src.bot.keyboards.root.undefined.callback_data import (
    UndefinedCallbackData,
    UndefinedAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(UndefinedCallbackData.filter(F.action == UndefinedAction.REJECT))
async def on_reject_undefined(
    c: types.CallbackQuery,
    callback_data: UndefinedCallbackData,
    uow: IUndefinedUoW,
    ftl: TranslatorRunner,
):
    await DeleteUndefined(uow)(callback_data.undefined_id)
    text = ftl.root.profile.registry.undefined.successfully.rejected()
    await c.message.delete()
    await c.message.answer(text)
