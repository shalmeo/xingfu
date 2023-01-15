from typing import TYPE_CHECKING

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner

from src.application.group.interfaces.uow import IGroupUoW
from src.application.group.usecases.group import GetGroup
from src.bot.constants import MISS
from src.bot.keyboards.root.groups.callback_data import GroupCallbackData, GroupAction
from src.bot.keyboards.root.groups.info import get_group_info_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(GroupCallbackData.filter(F.action == GroupAction.INFO))
async def on_group_info(
    c: types.CallbackQuery,
    callback_data: GroupCallbackData,
    state: FSMContext,
    base_url: str,
    ftl: TranslatorRunner,
    uow: IGroupUoW,
):
    group = await GetGroup(uow)(callback_data.group_id)
    teacher = f"{group.teacher.surname} {group.teacher.name}" if group.teacher else MISS
    text = ftl.root.profile.registry.group.info(
        name=group.name,
        teacher=teacher,
        description=group.description or MISS,
    )
    markup = get_group_info_markup(ftl, callback_data.group_id, base_url)
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()

    await state.update_data(group_id=str(callback_data.group_id))
