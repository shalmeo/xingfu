from typing import Protocol
from uuid import UUID

from src.application.teacher.dto.teacher import TeacherDTO
from src.domain.teacher.models.teacher import Teacher


class ITeacherReader(Protocol):
    async def get_teacher(self, teacher_id: UUID) -> TeacherDTO:
        ...

    async def get_teachers(self, offset: int, limit: int) -> list[TeacherDTO]:
        ...

    async def get_all(self) -> list[TeacherDTO]:
        ...

    async def get_teachers_count(self) -> int:
        ...


class ITeacherRepo(Protocol):
    async def get_teacher(self, teacher_id: UUID) -> Teacher:
        ...

    async def delete_teacher(self, teacher_id: UUID) -> None:
        ...

    async def add_teacher(self, teacher: Teacher) -> Teacher:
        ...

    async def update_teacher(self, teacher: Teacher) -> Teacher:
        ...
