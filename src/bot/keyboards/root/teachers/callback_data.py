from enum import Enum
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class TeacherAction(Enum):
    INFO = "INFO"
    DELETE = "DELETE"


class TeacherCallbackData(CallbackData, prefix="teacher"):
    teacher_id: UUID
    action: TeacherAction


class TeacherPageController(CallbackData, prefix="teacher_page"):
    offset: int
    limit: int
