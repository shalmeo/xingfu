from enum import Enum
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class GroupAction(Enum):
    INFO = "INFO"
    DELETE = "DELETE"
    TASKS = "TASKS"


class GroupCallbackData(CallbackData, prefix="group"):
    group_id: UUID
    action: GroupAction


class GroupPageController(CallbackData, prefix="group_page"):
    offset: int
    limit: int
