from typing import Optional
from uuid import UUID

from src.application.common.dto.common import BirthdayMixin
from src.application.undefined.dto.user import UserDTO


class UndefinedDTO(BirthdayMixin):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]

    user: UserDTO


class UndefinedCreateDTO(BirthdayMixin):
    name: str
    surname: str
    patronymic: Optional[str]
