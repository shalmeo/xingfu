from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AdminResponse(BaseModel):
    surname: str
    name: str
    patronymic: Optional[str]
    phone: Optional[str]
    telegram_id: Optional[int]
    telegram_username: Optional[str]
    birthday: str
    email: str
    level: Optional[str]
    description: Optional[str]
    timezone: str
    access_start: str
    access_end: str


class Admin(BaseModel):
    id: UUID
    name: str
    surname: str
    patronymic: Optional[str]


class AdminsReponse(BaseModel):
    admins: list[Admin]
