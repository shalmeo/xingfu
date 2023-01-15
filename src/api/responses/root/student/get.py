from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class StudentResponse(BaseModel):
    surname: str
    name: str
    patronymic: Optional[str]
    phone: Optional[str]
    telegram_id: Optional[int]
    telegram_username: Optional[str]
    birthday: str
    email: str
    timezone: str
    access_start: str
    access_end: str


class Student(BaseModel):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]


class StudentsReponse(BaseModel):
    students: list[Student]
