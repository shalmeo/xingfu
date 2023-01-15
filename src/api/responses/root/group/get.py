from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TeacherResponse(BaseModel):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]


class StudentResponse(BaseModel):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]


class GroupResponse(BaseModel):
    name: str
    description: Optional[str]
    teacher: Optional[TeacherResponse]
    students: list[StudentResponse]
