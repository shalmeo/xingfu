from datetime import date
from typing import Optional

from pydantic import BaseModel


class StudentCreateRequest(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str]
    phone: Optional[int]
    telegram_id: Optional[int]
    telegram_username: Optional[str]
    birthday: date
    email: str
    timezone: str
