from typing import TYPE_CHECKING

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format
from fluentogram import TranslatorRunner

from src.bot.states.student.current_works import CurrentWorks
from src.bot.states.student.done_works import DoneWorks
from src.bot.states.student.pending_works import PendingWorks
from src.bot.states.student.profile import Profile
from src.bot.states.student.wom_works import WomWorks

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


async def getter(dialog_manager: DialogManager, ftl: TranslatorRunner, **_):
    return {
        "student-profile-text": ftl.student.profile.text(),
        "student-profile-work-current-button": ftl.student.profile.work.current.button(),
        "student-profile-work-pending-button": ftl.student.profile.work.pending.button(),
        "student-profile-work-done-button": ftl.student.profile.work.done.button(),
        "student-profile-work-wom-button": ftl.student.profile.work.wom.button(),
    }


dialog = Dialog(
    Window(
        Format("{student-profile-text}"),
        Start(
            Format("student-profile-work-current-button"),
            id="curr_works",
            state=CurrentWorks.select_group,
        ),
        Start(
            Format("student-profile-work-pending-button"),
            id="pend_works",
            state=PendingWorks.select_work,
        ),
        Start(
            Format("student-profile-work-done-button"),
            id="done_works",
            state=DoneWorks.select_work,
        ),
        Start(
            Format("student-profile-work-wom-button"),
            id="wom_works",
            state=WomWorks.select_work,
        ),
        state=Profile.select_option,
        getter=getter,
    ),
)
