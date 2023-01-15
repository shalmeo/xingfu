from datetime import date
from typing import Optional

from pydantic import BaseModel


class AdminCreateRequest(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str]
    phone: Optional[int]
    telegram_id: Optional[int]
    telegram_username: Optional[str]
    birthday: date
    email: str
    level: Optional[str]
    description: Optional[str]
    timezone: str
