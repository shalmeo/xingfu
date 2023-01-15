from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from fluentogram import TranslatorRunner

from src.application.common.exceptions.common import OffsetNegative
from src.application.common.usecases.common import get_paginate
from src.application.group.interfaces.uow import IGroupUoW
from src.application.group.usecases.group import GetGroups, GetGroupsCount
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.groups.callback_data import GroupPageController
from src.bot.keyboards.root.groups.registry import get_groups_registry_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(ProfileCallbackData.filter(F.action == Registry.GROUPS))
async def on_groups_registry(
    c: types.CallbackQuery,
    state: FSMContext,
    base_url: str,
    uow: IGroupUoW,
    ftl: TranslatorRunner,
):
    offset, limit = 0, 9
    groups = await GetGroups(uow)(offset, limit)
    count = await GetGroupsCount(uow)()
    paginate = get_paginate(count, offset, limit)
    text = ftl.root.profile.registry.groups.text()
    markup = get_groups_registry_markup(ftl, groups, paginate, base_url)
    m = await c.message.edit_text(text, reply_markup=markup)
    await c.answer()

    await state.update_data(last_mid=m.message_id)


@router.callback_query(GroupPageController.filter())
async def page_controller(
    c: types.CallbackQuery,
    callback_data: GroupPageController,
    base_url: str,
    uow: IGroupUoW,
    ftl: TranslatorRunner,
):
    try:
        groups = await GetGroups(uow)(callback_data.offset, callback_data.limit)
    except OffsetNegative:
        await c.answer()
        return

    count = await GetGroupsCount(uow)()
    paginate = get_paginate(count, callback_data.offset, callback_data.limit)

    if 1 <= paginate.current_page <= paginate.pages:
        markup = get_groups_registry_markup(ftl, groups, paginate, base_url)
        with suppress(TelegramAPIError):
            await c.message.edit_reply_markup(markup)
    await c.answer()
