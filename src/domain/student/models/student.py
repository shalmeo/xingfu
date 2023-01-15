import datetime
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from src.domain.common.models.entity import Entity


class Student(Entity):
    id: UUID = Field(default_factory=uuid4)
    user_id: Optional[int]
    name: str
    surname: str
    patronymic: Optional[str]
    birthday: date

    access_start: date = Field(default_factory=uuid4)
    access_end: date = Field(default_factory=uuid4)


def access_start_default():
    return datetime.date.today()


def access_end_default():
    return datetime.date.today() + datetime.timedelta(days=365 * 10)
