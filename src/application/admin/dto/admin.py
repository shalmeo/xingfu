from typing import Optional
from uuid import UUID

from src.application.admin.dto.user import UserDTO
from src.application.common.dto.common import (
    AnimalMixin,
    BirthdayMixin,
    AccessDatesMixin,
)


class AdminDTO(AnimalMixin, BirthdayMixin, AccessDatesMixin):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]
    level: Optional[str]
    description: Optional[str]

    user: UserDTO


class AdminCreateDTO(BirthdayMixin):
    name: str
    surname: str
    patronymic: Optional[str]

    level: Optional[str]
    description: Optional[str]


class AdminUpdateDTO(BirthdayMixin, AccessDatesMixin):
    id: UUID

    name: str
    surname: str
    patronymic: Optional[str]

    level: Optional[str]
    description: Optional[str]
