from enum import Enum
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from src.domain.user.models.user import UserRole


class UndefinedAction(Enum):
    INFO = "INFO"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"


class UndefinedCallbackData(CallbackData, prefix="uncert"):
    undefined_id: UUID
    action: UndefinedAction


class UndefinedPageController(CallbackData, prefix="uncert_page"):
    offset: int
    limit: int


class UndefinedAcceptRoleCallbackData(CallbackData, prefix="uncert_role"):
    undefined_id: UUID
    role: UserRole
