from typing import Optional
from uuid import UUID

from src.application.common.dto.common import (
    AnimalMixin,
    BirthdayMixin,
    AccessDatesMixin,
)
from src.application.student.dto.creator import CreatorDTO
from src.application.student.dto.user import UserDTO


class StudentDTO(AnimalMixin, BirthdayMixin, AccessDatesMixin):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]

    creator: CreatorDTO
    user: UserDTO

    @property
    def school_nickname(self):
        return f"{self.name}{self.animal}"


class StudentCreateDTO(BirthdayMixin):
    name: str
    surname: str
    patronymic: Optional[str]


class StudentUpdateDTO(BirthdayMixin, AccessDatesMixin):
    id: UUID

    name: str
    surname: str
    patronymic: Optional[str]
