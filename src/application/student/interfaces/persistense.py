from typing import Protocol
from uuid import UUID

from src.application.student.dto.student import StudentDTO
from src.domain.student.models.student import Student


class IStudentReader(Protocol):
    async def get_student(self, teacher_id: UUID) -> StudentDTO:
        ...

    async def get_students(self, offset: int, limit: int) -> list[StudentDTO]:
        ...

    async def get_students_count(self) -> int:
        ...

    async def get_all(self) -> list[StudentDTO]:
        ...

    async def get_group_students(
        self, group_id: UUID, offset: int, limit: int
    ) -> list[StudentDTO]:
        ...

    async def get_group_students_count(self, group_id: UUID) -> int:
        ...


class IStudentRepo(Protocol):
    async def get_student(self, student_id: UUID) -> Student:
        ...

    async def delete_student(self, student_id: UUID) -> None:
        ...

    async def add_student(self, student: Student) -> Student:
        ...

    async def update_student(self, student: Student) -> Student:
        ...
