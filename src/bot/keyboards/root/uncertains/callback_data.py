from enum import Enum
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from src.domain.user.models.user import UserRole


class UncertainAction(Enum):
    INFO = "INFO"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"


class UncertainCallbackData(CallbackData, prefix="uncert"):
    uncertain_id: UUID
    action: UncertainAction


class UncertainPageController(CallbackData, prefix="uncert_page"):
    offset: int
    limit: int


class UncertainAcceptRoleCallbackData(CallbackData, prefix="uncert_role"):
    uncertain_id: UUID
    role: UserRole
