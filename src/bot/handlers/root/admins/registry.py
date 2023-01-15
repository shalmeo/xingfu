from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from fluentogram import TranslatorRunner

from src.application.common.exceptions.common import OffsetNegative
from src.application.common.usecases.common import get_paginate
from src.application.admin.interfaces.uow import IAdminUoW
from src.application.admin.usecases.admin import GetAdmins, GetAdminsCount
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.admins.callback_data import AdminPageController
from src.bot.keyboards.root.admins.registry import get_admins_registry_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(ProfileCallbackData.filter(F.action == Registry.ADMINS))
async def on_admins_registry(
    c: types.CallbackQuery,
    state: FSMContext,
    base_url: str,
    uow: IAdminUoW,
    ftl: TranslatorRunner,
):
    offset, limit = 0, 9
    admins = await GetAdmins(uow)(offset, limit)
    count = await GetAdminsCount(uow)()
    paginate = get_paginate(count, offset, limit)
    text = ftl.root.profile.registry.admins.text()
    markup = get_admins_registry_markup(ftl, admins, paginate, base_url)
    m = await c.message.edit_text(text, reply_markup=markup)
    await c.answer()

    await state.update_data(last_mid=m.message_id)


@router.callback_query(AdminPageController.filter())
async def page_controller(
    c: types.CallbackQuery,
    callback_data: AdminPageController,
    base_url: str,
    uow: IAdminUoW,
    ftl: TranslatorRunner,
):
    try:
        admins = await GetAdmins(uow)(callback_data.offset, callback_data.limit)
    except OffsetNegative:
        await c.answer()
        return

    count = await GetAdminsCount(uow)()
    paginate = get_paginate(count, callback_data.offset, callback_data.limit)

    if 1 <= paginate.current_page <= paginate.pages:
        markup = get_admins_registry_markup(ftl, admins, paginate, base_url)
        with suppress(TelegramAPIError):
            await c.message.edit_reply_markup(markup)
    await c.answer()
