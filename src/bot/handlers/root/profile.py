from typing import TYPE_CHECKING

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner

from src.bot.keyboards.root.profile import get_profile_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.message(Text(text="Профиль"))
async def on_profile(
    e: types.Message | types.CallbackQuery,
    state: FSMContext,
    ftl: TranslatorRunner,
):
    markup = get_profile_markup(ftl)
    text = ftl.root.profile.text()
    await e.answer(text, reply_markup=markup)
    await state.clear()


@router.callback_query(Text("to_profile"))
async def to_profile(
    c: types.CallbackQuery,
    state: FSMContext,
    ftl: TranslatorRunner,
):
    markup = get_profile_markup(ftl)
    text = ftl.root.profile.text()
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()
    await state.clear()
