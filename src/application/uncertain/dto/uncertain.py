from typing import Optional
from uuid import UUID

from src.application.common.dto.common import BirthdayMixin
from src.application.uncertain.dto.user import UserDTO


class UncertainDTO(BirthdayMixin):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]

    user: UserDTO


class UncertainCreateDTO(BirthdayMixin):
    name: str
    surname: str
    patronymic: Optional[str]
