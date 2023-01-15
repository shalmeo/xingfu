from typing import TYPE_CHECKING

from aiogram import Router, F, types
from fluentogram import TranslatorRunner

from src.application.uncertain.interfaces.uow import IUncertainUoW
from src.application.uncertain.usecases.uncertain import DetermineUncertain
from src.bot.keyboards.root.uncertains.accept import get_uncertain_accept_markup
from src.bot.keyboards.root.uncertains.callback_data import (
    UncertainCallbackData,
    UncertainAction,
    UncertainAcceptRoleCallbackData,
)
from src.domain.user.models.user import UserRole

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(UncertainCallbackData.filter(F.action == UncertainAction.ACCEPT))
async def on_accept_uncertain(
    c: types.CallbackQuery,
    callback_data: UncertainCallbackData,
    ftl: TranslatorRunner,
):
    text = (
        c.message.html_text + "\n\n" + ftl.root.profile.registry.uncertain.select.role()
    )
    markup = get_uncertain_accept_markup(ftl, callback_data.uncertain_id)
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()


@router.callback_query(UncertainAcceptRoleCallbackData.filter())
async def on_uncertain_accept_role(
    c: types.CallbackQuery,
    callback_data: UncertainAcceptRoleCallbackData,
    uow: IUncertainUoW,
    ftl: TranslatorRunner,
):
    await DetermineUncertain(uow)(callback_data.uncertain_id, callback_data.role)
    text = ftl.root.profile.registry.uncertain.successfully.added()
    await c.message.delete()
    await c.message.answer(text)
