from enum import Enum
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class StudentAction(Enum):
    INFO = "INFO"
    DELETE = "DELETE"


class StudentCallbackData(CallbackData, prefix="student"):
    student_id: UUID
    action: StudentAction


class StudentPageController(CallbackData, prefix="student_page"):
    offset: int
    limit: int
