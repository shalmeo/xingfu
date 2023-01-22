from typing import TYPE_CHECKING

from aiogram import Router, F, types
from fluentogram import TranslatorRunner

from src.application.undefined.interfaces.uow import IUndefinedUoW
from src.application.undefined.usecases.undefined import DetermineUndefined
from src.bot.keyboards.root.undefined.accept import get_undefined_accept_markup
from src.bot.keyboards.root.undefined.callback_data import (
    UndefinedCallbackData,
    UndefinedAction,
    UndefinedAcceptRoleCallbackData,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(UndefinedCallbackData.filter(F.action == UndefinedAction.ACCEPT))
async def on_accept_undefined(
    c: types.CallbackQuery,
    callback_data: UndefinedCallbackData,
    ftl: TranslatorRunner,
):
    text = c.message.html_text + "\n\n" + ftl.root.profile.registry.undefined.select.role()
    markup = get_undefined_accept_markup(ftl, callback_data.undefined_id)
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()


@router.callback_query(UndefinedAcceptRoleCallbackData.filter())
async def on_undefined_accept_role(
    c: types.CallbackQuery,
    callback_data: UndefinedAcceptRoleCallbackData,
    uow: IUndefinedUoW,
    ftl: TranslatorRunner,
):
    await DetermineUndefined(uow)(callback_data.undefined_id, callback_data.role)
    text = ftl.root.profile.registry.undefined.successfully.added()
    await c.message.delete()
    await c.message.answer(text)
