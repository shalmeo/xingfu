from typing import Optional
from uuid import UUID

from src.application.common.dto.common import DTO
from src.application.group.dto.creator import CreatorDTO
from src.application.group.dto.student import StudentDTO
from src.application.group.dto.teacher import TeacherDTO


class GroupDTO(DTO):
    id: UUID

    name: str
    description: Optional[str]

    creator: CreatorDTO
    teacher: Optional[TeacherDTO]
    students: list[StudentDTO]


class GroupCreateDTO(DTO):
    name: str
    description: Optional[str]
    teacher_id: Optional[UUID]
    students: list[UUID]


class GroupUpdateDTO(DTO):
    id: UUID

    name: str
    description: Optional[str]
    teacher_id: Optional[UUID]
    students: list[UUID]
