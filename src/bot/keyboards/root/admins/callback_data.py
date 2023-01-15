from enum import Enum
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class AdminAction(Enum):
    INFO = "INFO"
    DELETE = "DELETE"


class AdminCallbackData(CallbackData, prefix="admin"):
    admin_id: UUID
    action: AdminAction


class AdminPageController(CallbackData, prefix="admin_page"):
    offset: int
    limit: int
