from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from fluentogram import TranslatorRunner

from src.application.common.exceptions.common import OffsetNegative
from src.application.common.usecases.common import get_paginate
from src.application.uncertain.interfaces.uow import IUncertainUoW
from src.application.uncertain.usecases.uncertain import (
    GetUncertains,
    GetUncertainsCount,
)
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.uncertains.callback_data import UncertainPageController
from src.bot.keyboards.root.uncertains.registry import get_uncertains_registry_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(ProfileCallbackData.filter(F.action == Registry.UNCERTAINS))
async def on_uncertains_registry(
    c: types.CallbackQuery,
    state: FSMContext,
    uow: IUncertainUoW,
    ftl: TranslatorRunner,
):
    offset, limit = 0, 9
    uncertains = await GetUncertains(uow)(offset, limit)
    count = await GetUncertainsCount(uow)()
    paginate = get_paginate(count, offset, limit)
    text = ftl.root.profile.registry.uncertains.text()
    markup = get_uncertains_registry_markup(ftl, uncertains, paginate)
    m = await c.message.edit_text(text, reply_markup=markup)
    await c.answer()

    await state.update_data(last_mid=m.message_id)


@router.callback_query(UncertainPageController.filter())
async def page_controller(
    c: types.CallbackQuery,
    callback_data: UncertainPageController,
    uow: IUncertainUoW,
    ftl: TranslatorRunner,
):
    try:
        uncertains = await GetUncertains(uow)(callback_data.offset, callback_data.limit)
    except OffsetNegative:
        await c.answer()
        return

    count = await GetUncertainsCount(uow)()
    paginate = get_paginate(count, callback_data.offset, callback_data.limit)

    if 1 <= paginate.current_page <= paginate.pages:
        markup = get_uncertains_registry_markup(ftl, uncertains, paginate)
        with suppress(TelegramAPIError):
            await c.message.edit_reply_markup(markup)

    await c.answer()
