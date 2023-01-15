from typing import Optional
from pydantic import BaseModel


class StudentUpdateRequest(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str]
    telegram_id: Optional[int]
    telegram_username: Optional[str]
    email: str
    phone: Optional[int]
    timezone: str
    birthday: str
    access_start: str
    access_end: str