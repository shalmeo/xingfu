from typing import Optional
from uuid import UUID

from src.application.common.dto.common import DTO
from src.application.group.dto.user import UserDTO


class TeacherDTO(DTO):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]

    user: UserDTO
