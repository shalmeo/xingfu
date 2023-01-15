from typing import Optional
from uuid import UUID

from src.application.common.dto.common import (
    AnimalMixin,
    BirthdayMixin,
    AccessDatesMixin,
)
from src.application.teacher.dto.creator import CreatorDTO
from src.application.teacher.dto.user import UserDTO


class TeacherDTO(AnimalMixin, BirthdayMixin, AccessDatesMixin):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]
    level: Optional[str]
    description: Optional[str]

    creator: CreatorDTO
    user: UserDTO

    @property
    def school_nickname(self):
        return f"{self.name} {self.patronymic}{self.animal}"


class TeacherCreateDTO(BirthdayMixin):
    name: str
    surname: str
    patronymic: Optional[str]

    level: Optional[str]
    description: Optional[str]


class TeacherUpdateDTO(BirthdayMixin, AccessDatesMixin):
    id: UUID

    name: str
    surname: str
    patronymic: Optional[str]

    level: Optional[str]
    description: Optional[str]
