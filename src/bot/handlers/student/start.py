from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner



router = Router()


@router.message(Command("start"), StateFilter("*"))
async def on_cmd_start(m: types.Message, ftl: TranslatorRunner):
    text = ftl.start.welcome()
    # markup = get_start_markup(ftl)
    await m.answer(text)