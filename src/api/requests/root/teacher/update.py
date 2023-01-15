from typing import Optional
from pydantic import BaseModel


class TeacherUpdateRequest(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str]
    telegram_id: Optional[int]
    telegram_username: Optional[str]
    email: str
    phone: Optional[int]
    timezone: str
    level: Optional[str]
    description: Optional[str]
    birthday: str
    access_start: str
    access_end: str