from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from fluentogram import TranslatorRunner

from src.application.common.exceptions.common import OffsetNegative
from src.application.common.usecases.common import get_paginate
from src.application.undefined.interfaces.uow import IUndefinedUoW
from src.application.undefined.usecases.undefined import (
    GetUndefineds,
    GetUndefinedsCount,
)
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.undefined.callback_data import UndefinedPageController
from src.bot.keyboards.root.undefined.registry import get_undefineds_registry_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(ProfileCallbackData.filter(F.action == Registry.UNCERTAINS))
async def on_undefineds_registry(
    c: types.CallbackQuery,
    state: FSMContext,
    uow: IUndefinedUoW,
    ftl: TranslatorRunner,
):
    offset, limit = 0, 9
    undefineds = await GetUndefineds(uow)(offset, limit)
    count = await GetUndefinedsCount(uow)()
    paginate = get_paginate(count, offset, limit)
    text = ftl.root.profile.registry.undefineds.text()
    markup = get_undefineds_registry_markup(ftl, undefineds, paginate)
    m = await c.message.edit_text(text, reply_markup=markup)
    await c.answer()

    await state.update_data(last_mid=m.message_id)


@router.callback_query(UndefinedPageController.filter())
async def page_controller(
    c: types.CallbackQuery,
    callback_data: UndefinedPageController,
    uow: IUndefinedUoW,
    ftl: TranslatorRunner,
):
    try:
        undefineds = await GetUndefineds(uow)(callback_data.offset, callback_data.limit)
    except OffsetNegative:
        await c.answer()
        return

    count = await GetUndefinedsCount(uow)()
    paginate = get_paginate(count, callback_data.offset, callback_data.limit)

    if 1 <= paginate.current_page <= paginate.pages:
        markup = get_undefineds_registry_markup(ftl, undefineds, paginate)
        with suppress(TelegramAPIError):
            await c.message.edit_reply_markup(markup)

    await c.answer()
