from uuid import UUID

from src.domain.group.models.stuent import Student


def create_student(id: UUID) -> Student:
    return Student(id=id)