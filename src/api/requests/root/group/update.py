from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Teacher(BaseModel):
    id: UUID
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]


class Student(BaseModel):
    id: UUID
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]


class GroupUpdateRequest(BaseModel):
    name: str
    description: Optional[str]
    teacher: Teacher
    students: list[Student]
